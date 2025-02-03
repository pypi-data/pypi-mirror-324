# **OptimaLab35**
_Last updated: 02 Feb 2025 (v.0.9.0)_

## **Overview**

**OptimaLab35** enhances **OPTIMA35** (**Organizing, Processing, Tweaking Images, and Modifying scanned Analogs from 35mm Film**) by offering a user-friendly graphical interface for efficient image and metadata management.

It serves as a GUI for the [OPTIMA35 library](https://gitlab.com/CodeByMrFinchum/optima35), providing an intuitive way to interact with the core functionalities.

---

## **Current Status**
### **Early Development**
OptimaLab35 is actively developed using **PySide6** and **Qt**, providing a modern interface for **OPTIMA35**.

The program is still in its early stages, and features may change drastically over time. Some features might be added but later removed if they don't prove useful. Expect significant changes to the UI and functionality between updates.

For the most accurate and detailed update information, please refer to the [**CHANGELOG**](https://gitlab.com/CodeByMrFinchum/OptimaLab35/-/blob/main/CHANGELOG.md) as the readme might lack behind.

---

## **Features**

### **Image Processing**
- Resize images (upscale or downscale)
- Convert images to grayscale
- Adjust brightness and contrast
- Add customizable text-based watermarks

### **Image Preview**
- Load a single image and see how changes in brightness and contrast affect the image

### **EXIF Management**
- Add EXIF data using a simple dictionary
- Copy EXIF data from the original image
- Remove EXIF metadata completely
- Add timestamps (e.g., original photo timestamp)
- Automatically adjust EXIF timestamps based on image file names
- Add GPS coordinates to images

### **Updater**
- Checks for updates on PyPI, automatically downloads and installs the latest version
- Restarts the program after update

---

## **Installation**

Install via **pip** (dependencies are handled automatically):
```bash
pip install OptimaLab35
```

---

## Preview GUI **0.9.0**
**PREVIEW** might be out of date.

**Main tab**

![main](https://gitlab.com/CodeByMrFinchum/OptimaLab35/-/raw/main/media/main_tab.png){width=40%}

**Exif tab**

![main](https://gitlab.com/CodeByMrFinchum/OptimaLab35/-/raw/main/media/exif_tab.png){width=40%}

**Exif editor**

![main](https://gitlab.com/CodeByMrFinchum/OptimaLab35/-/raw/main/media/exif_editor.png){width=40%}

**Preview window**

![main](https://gitlab.com/CodeByMrFinchum/OptimaLab35/-/raw/main/media/preview_window.png){width=40%}

**About**

![main](https://gitlab.com/CodeByMrFinchum/OptimaLab35/-/raw/main/media/about_window.png){width=40%}

**Updater**

![main](https://gitlab.com/CodeByMrFinchum/OptimaLab35/-/raw/main/media/updater_window.png){width=40%}

---

# Use of LLMs
In the interest of transparency, I disclose that Generative AI (GAI) large language models (LLMs), including OpenAI’s ChatGPT and Ollama models (e.g., OpenCoder and Qwen2.5-coder), have been used to assist in this project.

## Areas of Assistance:
- Project discussions and planning
- Spelling and grammar corrections
- Suggestions for suitable packages and libraries
- Guidance on code structure and organization

In cases where LLMs contribute directly to code or provide substantial optimizations, such contributions will be disclosed and documented in the relevant sections of the codebase.

**Ollama**
- mradermacher gguf Q4K-M Instruct version of infly/OpenCoder-1.5B
- unsloth gguf Q4K_M Instruct version of both Qwen/QWEN2 1.5B and 3B

### References
1. **Huang, Siming, et al.**
   *OpenCoder: The Open Cookbook for Top-Tier Code Large Language Models.*
   2024. [PDF](https://arxiv.org/pdf/2411.04905)

2. **Hui, Binyuan, et al.**
   *Qwen2.5-Coder Technical Report.*
   *arXiv preprint arXiv:2409.12186*, 2024. [arXiv](https://arxiv.org/abs/2409.12186)

3. **Yang, An, et al.**
   *Qwen2 Technical Report.*
   *arXiv preprint arXiv:2407.10671*, 2024. [arXiv](https://arxiv.org/abs/2407.10671)
