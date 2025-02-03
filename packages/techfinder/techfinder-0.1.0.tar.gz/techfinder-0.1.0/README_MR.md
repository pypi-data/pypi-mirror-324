

# Detector

**Detector** हे एक Python लायब्ररी आहे जे वेबसाइट्सवरील तंत्रज्ञानांची ओळख पटवते. ही लायब्ररी HTML सामग्री आणि HTTP हेडर्सवर आधारित विविध तंत्रज्ञानांचा शोध घेत असते, जसे की फ्रेमवर्क्स, लायब्ररीज आणि सर्व्हर सॉफ़्टवेअर. यामध्ये डिफॉल्ट पॅटर्न्ससह, यूझरने डिफाइन केलेल्या कस्टम पॅटर्न्सला सपोर्ट केला जातो.

## वैशिष्ट्ये
- **तंत्रज्ञान ओळख**: वेबसाइटवरील विविध तंत्रज्ञानांचा शोध लावतो, जसे की फ्रेमवर्क्स (उदाहरणार्थ, React, Angular), सर्व्हर तंत्रज्ञान (उदाहरणार्थ, Apache, Nginx), आणि क्लाउड सेवा (उदाहरणार्थ, AWS, Google Cloud).
- **कस्टम पॅटर्न्स**: वापरकर्ते त्यांच्या कस्टम तंत्रज्ञान ओळखण्यासाठी JSON फाइलद्वारे पॅटर्न्स डिफाइन करू शकतात.
- **HTML आणि HTTP हेडर पॅर्सिंग**: HTML सामग्री आणि HTTP हेडर्स दोन्हीचे विश्लेषण करून तंत्रज्ञान ओळखले जातात.
- **विस्तारणीय**: अतिरिक्त तंत्रज्ञान ओळखण्यासाठी सहजपणे विस्तारता येणारे.

## स्थापना/Installation

**Detector** लायब्ररी स्थापित/Installation करण्यासाठी खालील आदेश वापरा:

```bash
pip install detector
```

किंवा, या रिपॉझिटरीला क्लोन करून निर्भरता मॅन्युअली स्थापित करा:

```bash
git clone https://github.com/Prathameshsci369/Detector.git
cd Detector
pip install -r requirements.txt
```

## वापर

### आयात आणि प्रारंभ

प्रथम, **Detector** क्लास आयात करा:

```python
from detector import Detector
```

आपण डिफॉल्ट पॅटर्न्ससह डिटेक्टर प्रारंभ करू शकता किंवा आपली कस्टम JSON फाइल प्रदान करून प्रारंभ करू शकता:

```python
# डिफॉल्ट पॅटर्न्ससह प्रारंभ करा
detector = Detector()

# कस्टम पॅटर्न्ससह प्रारंभ करा (कस्टम JSON कॉन्फिगचा पथ द्या)
detector = Detector('custom_patterns.json')
```

### बेसिक डिटेक्शन युज केस

वेबसाइटवर तंत्रज्ञान ओळखण्यासाठी `final_function` पद्धत वापरू शकता, जी URL प्राप्त करून त्याची HTML आणि हेडरचे विश्लेषण करते:

```python
url = 'https://example.com'
detected_tech = detector.final_function(url)

print("Detected Technologies:", detected_tech)
```

### कस्टम पॅटर्न्स

आपण स्वतःचे पॅटर्न्स तयार करू इच्छित असल्यास, एक कस्टम JSON फाइल तयार करू शकता:

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

त्यानंतर, आपण **Detector** ला या फाइलसह प्रारंभ करू शकता:

```python
detector = Detector('custom_patterns.json')
detected_tech = detector.final_function('https://example.com')
print("Detected Technologies:", detected_tech)
```

### उदाहरण आउटपुट

#### उदाहरण 1: डिफॉल्ट पॅटर्न्स

`https://example.com` सारख्या URL साठी, आउटपुट असे दिसू शकते:

```
Detected Technologies: ['React', 'Node.js', 'Express']
```

#### उदाहरण 2: कस्टम पॅटर्न्स

जर URL ने कस्टम पॅटर्न्सशी जुळले असेल, तर आउटपुट असे दिसू शकते:

```
Detected Technologies: ['MyCustomTech', 'MyCustomServer']
```

### लॉगिंग

**Detector** लायब्ररी Python च्या अंतर्निहित लॉगिंग मॉड्यूलचा वापर करून कार्यवाहीची माहिती प्रदान करते. डिफॉल्टने, ही लायब्ररी महत्त्वाच्या क्रियांची नोंद करते जसे की पॅटर्न लोडिंग आणि तंत्रज्ञान ओळखणे. आपल्याला आवश्यक असल्यास, आपण लॉगिंग लेव्हल कस्टमाइझ करू शकता:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # लॉगिंग लेव्हल DEBUG वर सेट करा
```

### त्रुटी हाताळणी

लायब्ररी सामान्य त्रुटी जसे की अवैध URL किंवा डेटा प्राप्त करत असताना एरर हॅंडल करते. जर काही चूक झाली तर लॉगमध्ये एरर संदेश दिसतील आणि प्रोग्राम चालू राहील.

```python
detected_tech = detector.final_function('https://invalid-url.com')
# लॉगमध्ये एरर दिसेल: "Error fetching the URL"
```

## युज केस

### युज केस 1: वेब फ्रेमवर्क्स आणि लायब्ररीज ओळखणे

**Detector** लायब्ररीचा वापर वेब फ्रेमवर्क्स आणि लायब्ररीज ओळखण्यासाठी केला जाऊ शकतो. उदाहरणार्थ, वेबसाइटवर React, Vue.js, किंवा Angular वापरणारे तंत्रज्ञान शोधणे.

```python
detector = Detector()
url = 'https://some-react-site.com'
detected_tech = detector.final_function(url)
print(detected_tech)  # अपेक्षित आउटपुट: ['React']
```

### युज केस 2: सर्व्हर तंत्रज्ञान ओळखणे

आपण वेबसाइटच्या सर्व्हर-साइड तंत्रज्ञानाची ओळख पटवण्यासाठी या लायब्ररीचा वापर करू शकता, जसे Apache, Nginx, किंवा AWS सारख्या क्लाउड प्लॅटफॉर्म्स.

```python
detector = Detector()
url = 'https://some-apache-server.com'
detected_tech = detector.final_function(url)
print(detected_tech)  # अपेक्षित आउटपुट: ['Apache']
```

### युज केस 3: विशिष्ट तंत्रज्ञानांसाठी कस्टम पॅटर्न्स डिफाइन करणे

जर डिफॉल्ट पॅटर्न्समध्ये नसलेल्या तंत्रज्ञानाची ओळख पटवायची असेल, तर आपण कस्टम JSON फाइलद्वारे तंत्रज्ञान ओळख पॅटर्न्स डिफाइन करू शकता.

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

हे पॅटर्न्स वापरून आपण तंत्रज्ञान ओळख करू शकता.

### युज केस 4: तंत्रज्ञान बदलांची निगराणी करणे

आपण **Detector** लायब्ररीला आपल्या निगराणी टूल्समध्ये एकत्र करून, विविध वेबसाइट्सवरील तंत्रज्ञान बदलांची वेळोवेळी तपासणी करू शकता.

```python
detector = Detector()
url = 'https://example.com'
detected_tech = detector.final_function(url)
# प्रत्येक आठवड्यात तंत्रज्ञान ओळखली जाईल
```

## योगदान

आम्ही **Detector** लायब्ररीमध्ये योगदानाचे स्वागत करतो! जर आपल्याला बग रिपोर्ट करायचे असतील, नवीन फीचर्स सुचवायच्या असतील किंवा code सुधारायचे असतील, तर कृपया एक इश्यू उघडा किंवा पुल pull request सादर करा.

