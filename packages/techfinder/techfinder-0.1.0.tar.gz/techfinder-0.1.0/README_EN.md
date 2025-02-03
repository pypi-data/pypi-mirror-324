

# Detector

**Detector** is a Python library designed to detect technologies used on websites. It checks both the HTML content and HTTP headers of a given URL to identify various technologies like frameworks, libraries, and server software. The library provides both default patterns and support for user-defined patterns via a JSON configuration file.

## Features
- **Technology Detection**: Detects web technologies such as frameworks (e.g., React, Angular), server technologies (e.g., Apache, Nginx), and cloud services (e.g., AWS, Google Cloud).
- **Custom Patterns**: Users can define their own patterns for technology detection via a custom JSON file.
- **HTML and HTTP Header Parsing**: Examines both HTML content and HTTP headers to identify technologies.
- **Extensible**: Easily extendable to support additional technologies by updating the patterns.

## Installation

To install the **Detector** library, run the following command:

```bash
pip install detector
```

Alternatively, clone this repository and install dependencies manually:

```bash
git clone https://github.com/Prathameshsci369/Detector.git
cd Detector
pip install -r requirements.txt
```

## Usage

### Importing and Initializing

First, import the **Detector** class:

```python
from detector import Detector
```

You can initialize the detector with a default pattern set or provide a custom JSON file containing user-defined patterns.

```python
# Initialize with default patterns
detector = Detector()

# Initialize with custom patterns (provide path to your custom JSON config)
detector = Detector('custom_patterns.json')
```

### Basic Detection Use Case

To detect technologies from a website, you can use the `final_function` method, which fetches the URL and analyzes its HTML and headers:

```python
url = 'https://example.com'
detected_tech = detector.final_function(url)

print("Detected Technologies:", detected_tech)
```

### Custom Patterns

If you want to use your own patterns to detect specific technologies, you can create a custom JSON file like the one below:

**custom_patterns.json**

```json
{
  "html_patterns": {
    "MyCustomTech": "mycustomtech"
  },
  "header_patterns": {
    "MyCustomServer": "mycustomserver"
  }
}
```

You can then initialize **Detector** with this file:

```python
detector = Detector('custom_patterns.json')
detected_tech = detector.final_function('https://example.com')
print("Detected Technologies:", detected_tech)
```

### Example Outputs

#### Example 1: Default Patterns

For a URL like `https://example.com`, the output might be:

```
Detected Technologies: ['React', 'Node.js', 'Express']
```

#### Example 2: Custom Patterns

If the URL matches custom patterns in `custom_patterns.json`, the output might look like:

```
Detected Technologies: ['MyCustomTech', 'MyCustomServer']
```

### Logging

The **Detector** library uses Python's built-in logging module to provide detailed information during execution. By default, it logs important actions such as pattern loading and technology detection. You can customize the logging level as needed:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # Change logging level to DEBUG
```

### Error Handling

The library will handle common errors such as invalid URLs or issues with fetching data gracefully. If something goes wrong, you will see an error message in the logs, and the program will continue running.

```python
detected_tech = detector.final_function('https://invalid-url.com')
# Will log an error: "Error fetching the URL"
```

## Use Cases

### Use Case 1: Identify Web Frameworks and Libraries

**Detector** can be used to determine what frameworks and libraries a website is using. For example, detecting if a website uses React, Vue.js, or Angular.

```python
detector = Detector()
url = 'https://some-react-site.com'
detected_tech = detector.final_function(url)
print(detected_tech)  # Expected output: ['React']
```

### Use Case 2: Identify Server Technologies

You can use this library to detect the server-side technology used by a website, such as Apache, Nginx, or a cloud platform like AWS.

```python
detector = Detector()
url = 'https://some-apache-server.com'
detected_tech = detector.final_function(url)
print(detected_tech)  # Expected output: ['Apache']
```

### Use Case 3: Customize Patterns for Specific Technologies

If you have specific technologies that are not part of the default set, you can define your own patterns in a custom JSON file.

```json
{
  "html_patterns": {
    "MyCustomTech": "mycustomtech"
  },
  "header_patterns": {
    "MyCustomServer": "mycustomserver"
  }
}
```

This allows you to track and detect technologies that are unique to your environment or your use case.

### Use Case 4: Monitor Technology Changes

By integrating **Detector** into your monitoring tools, you can keep track of which technologies are being used on various websites over time. This could be useful for identifying when websites update their tech stack.

```python
detector = Detector()
url = 'https://example.com'
detected_tech = detector.final_function(url)
# Log detected technologies every week
```

## Contributing

We welcome contributions to the **Detector** library! If you'd like to report bugs, suggest new features, or help improve the documentation, feel free to open an issue or submit a pull request.

