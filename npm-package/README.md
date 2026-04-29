# placeholder-img

Client SDK for the [Placeholder Image API](https://placeholder-api.surge.sh). Generate placeholder images with a single function call.

## Installation

```bash
npm install placeholder-img
```

## Usage

### Get a placeholder image URL

```js
const placeholder = require('placeholder-img');

// Simple URL
const url = placeholder(300, 200);
// => "https://placeholder-api.surge.sh/300x200.png"

// Using .url() — same result
const url2 = placeholder.url(300, 200);
```

### Custom options

```js
const url = placeholder.url(400, 300, {
  bgColor: '336699',    // background color (hex, no #)
  textColor: 'ffffff',   // text color
  text: 'Hello!',       // custom text
  format: 'jpg'         // png (default), jpg, or webp
});
// => "https://placeholder-api.surge.sh/400x300.jpg?bg=336699&fg=ffffff&text=Hello!"
```

### Download image data

```js
// Promise-based
const buffer = await placeholder.download(300, 200, { format: 'png' });
// buffer is a Node Buffer with PNG image data

// Callback-based
placeholder.download(300, 200, { bgColor: 'cc0000' }, (err, buffer) => {
  if (err) throw err;
  // use buffer ...
});
```

### With API key

```js
const url = placeholder.url(300, 200, { apiKey: 'your-api-key' });
```

### Custom base URL

```js
const url = placeholder.url(300, 200, { baseUrl: 'http://149.202.58.157:8892' });
// => "http://149.202.58.157:8892/300x200.png"
```

## API

### `placeholder(width, height, options?)`

Alias for `placeholder.url()`. Returns a URL string.

### `placeholder.url(width, height, options?)`

Returns the full URL for the placeholder image.

| Parameter       | Type     | Default                         | Description                      |
|----------------|----------|---------------------------------|----------------------------------|
| `width`        | number   | — (required)                    | Image width in pixels             |
| `height`       | number   | — (required)                    | Image height in pixels           |
| `options.bgColor`  | string | —                             | Background color (hex, no #)     |
| `options.textColor`| string | —                             | Text color (hex, no #)           |
| `options.text`     | string | —                             | Custom overlay text              |
| `options.format`   | string | `"png"`                        | Image format: png, jpg, webp     |
| `options.apiKey`   | string | —                             | API key                          |
| `options.baseUrl`  | string | `"https://placeholder-api.surge.sh"` | Custom API base URL        |

### `placeholder.download(width, height, options?, callback?)`

Downloads the image and returns its data.

- **With callback**: Node-style `(err, buffer)` callback. Returns `undefined`.
- **Without callback**: Returns a `Promise<Buffer>`.

## License

MIT