# Network Tools

A simple network utilities web application built with Anvil.Works and styled using Pico CSS.

<img src="https://github.com/user-attachments/assets/9e82d640-98c8-4fc8-83e4-76ed8d8b1003" alt="Network Tools Screenshot" width="600">

## Features

- **Port Scanner** - Check if specific ports are open on a host
- **DNS Propagation** - Check DNS record propagation across multiple nameservers

## About the Implementation

This app demonstrates using custom HTML in Anvil with the [Pico CSS](https://picocss.com/) framework. Pico is a classless CSS framework, meaning it styles plain HTML tags without requiring custom classes - for example, `<button>Submit</button>` gets styled automatically.

The custom CSS has been kept minimal, included only to ensure Pico renders correctly within the Anvil environment.

## Links

- **[Try the live app](https://network-tools.anvil.app)**
- **[Clone this app on Anvil.Works](https://anvil.works/build#clone:ROVU7EWAK6BMFYRB=MXGQTLBXMDXIVE3TW466NPUY)**

## Customization

To change the color scheme, replace the CDN link in Native Libraries with a different theme from the [Pico CSS version picker](https://picocss.com/docs/version-picker):
```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.pumpkin.min.css"
>
```

## Resources

- [Pico CSS](https://picocss.com/)
- [Pico CSS Themes](https://picocss.com/docs/version-picker)
- [Anvil.Works](https://anvil.works)
