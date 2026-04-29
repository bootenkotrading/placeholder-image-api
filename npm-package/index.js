'use strict';

const https = require('https');
const http = require('http');
const url = require('url');

const DEFAULT_BASE_URL = 'https://placeholder-api.surge.sh';

/**
 * Build a placeholder image URL.
 *
 * @param {number} width   - Image width in pixels
 * @param {number} height  - Image height in pixels
 * @param {object} [options] - Optional settings
 * @param {string} [options.bgColor]   - Background color (hex without #, e.g. "336699")
 * @param {string} [options.textColor] - Text color (hex without #, e.g. "ffffff")
 * @param {string} [options.text]      - Custom text overlay
 * @param {string} [options.format]    - Image format: "png" (default), "jpg", or "webp"
 * @param {string} [options.apiKey]     - API key if required
 * @returns {string} The full URL for the placeholder image
 */
function buildUrl(width, height, options) {
  if (!width || !height) {
    throw new Error('width and height are required');
  }
  const opts = options || {};
  const format = opts.format || 'png';

  // Construct path: /<width>x<height>.<format>
  let path = `/${width}x${height}.${format}`;

  // Build query string from remaining options
  const query = {};
  if (opts.bgColor) query.bg = opts.bgColor;
  if (opts.textColor) query.fg = opts.textColor;
  if (opts.text) query.text = opts.text;
  if (opts.apiKey) query.key = opts.apiKey;

  const qs = Object.keys(query).length
    ? '?' + Object.entries(query).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&')
    : '';

  const base = opts.baseUrl || DEFAULT_BASE_URL;
  return `${base}${path}${qs}`;
}

/**
 * Return the URL string for a placeholder image.
 *
 * @param {number} width
 * @param {number} height
 * @param {object} [options]
 * @returns {string}
 */
function placeholderUrl(width, height, options) {
  return buildUrl(width, height, options);
}

/**
 * Download a placeholder image and return its Buffer.
 * If a callback is provided it follows Node-style (err, buffer) convention.
 * If no callback is provided, a Promise is returned.
 *
 * @param {number} width
 * @param {number} height
 * @param {object} [options]
 * @param {function} [callback] - Optional Node-style callback (err, buffer)
 * @returns {Promise<Buffer>|undefined}
 */
function placeholderDownload(width, height, options, callback) {
  if (typeof options === 'function') {
    callback = options;
    options = {};
  }
  const opts = options || {};
  const imageUrl = buildUrl(width, height, opts);

  function doRequest(cb) {
    const parsed = url.parse(imageUrl);
    const transport = parsed.protocol === 'https:' ? https : http;

    transport.get(imageUrl, { timeout: 30000 }, (res) => {
      // Follow redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return doRedirectRequest(res.headers.location, cb);
      }
      if (res.statusCode !== 200) {
        res.resume();
        return cb(new Error(`HTTP ${res.statusCode} for ${imageUrl}`));
      }
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => cb(null, Buffer.concat(chunks)));
      res.on('error', (err) => cb(err));
    }).on('error', (err) => cb(err));
  }

  function doRedirectRequest(location, cb) {
    const parsed = url.parse(location);
    const transport = parsed.protocol === 'https:' ? https : http;

    transport.get(location, { timeout: 30000 }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return doRedirectRequest(res.headers.location, cb);
      }
      if (res.statusCode !== 200) {
        res.resume();
        return cb(new Error(`HTTP ${res.statusCode} for ${location}`));
      }
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => cb(null, Buffer.concat(chunks)));
      res.on('error', (err) => cb(err));
    }).on('error', (err) => cb(err));
  }

  if (typeof callback === 'function') {
    doRequest(callback);
    return undefined;
  }

  return new Promise((resolve, reject) => {
    doRequest((err, buf) => {
      if (err) return reject(err);
      resolve(buf);
    });
  });
}

/**
 * Main entry point — called as placeholder(width, height, options)
 * Returns the URL by default (same as placeholder.url).
 *
 * @param {number} width
 * @param {number} height
 * @param {object} [options]
 * @returns {string} URL string
 */
function placeholder(width, height, options) {
  return buildUrl(width, height, options);
}

// Attach sub-methods
placeholder.url = placeholderUrl;
placeholder.download = placeholderDownload;

module.exports = placeholder;