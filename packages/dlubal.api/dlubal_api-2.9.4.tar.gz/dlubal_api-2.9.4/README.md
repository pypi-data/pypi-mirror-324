# Dlubal API 2.0

![PyPI](https://img.shields.io/pypi/v/dlubal.api)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-Proprietary-red)

## Overview
The `dlubal.api` package is the next-generation Python client library for interacting with Dlubal Software APIs, leveraging modern **gRPC technology** to deliver high-speed communication, scalability, and improved performance. This API enables **seamless automation** and **remote access** to Dlubal software like **RFEM 6**, with near future support for **RSTAB 9** and **RSECTION 1**.

## Key Features
- **Unified API**: Works across all Dlubal applications, starting with **RFEM**.
- **Performance Boost**: 5-10x faster execution than previous implementations.
- **Seamless Model Export**: Generate Python scripts directly from RFEM models.
- **Blocks & Components**: Define reusable components for efficient model parametrization.
- **AI-Driven Tools**: Leverage AI-based features (e.g., **MIA** powered by structured data).
- **Flexible Licensing**: Supports **on-premises** and **cloud-based** workflows.
- **Secure & Scalable**: API authentication via API keys, with **fine-grained access control**.

---

## Installation

Ensure you have **Python 3.10+** installed. Then, install the package via **pip**:

```sh
pip install dlubal.api
```

For additional installation options, refer to the **official documentation**.

---

## Quick Start

### Authentication & Authorization
To access the API, you need:
- **Authentication**: API Keys which can be generated in your Extranet user account under the API & Cloud Dashboard.
- **Authorization**: Active API Service subscription (license-based).

Be aware, certain API methods are monetized by **API Credits**!.

---

### Example Usage
```python
import dlubal.api.rfem

with rfem.Application(api_key="your_api_key") as rfem_app:
    # Example API call
    rfem_app.create_model("MyModel")
    rfem_app.create_object(
        rfem.structure_core.Node(coordinate_1=2)
    )
```

## Documentation & Support
- 📖 **API Documentation**: [API Docs](https://www.dlubal.com/en/solutions/dlubal-api/api-documentation/index)
- 💬 **Support**: Contact [Dlubal Support](https://www.dlubal.com/en/support-and-learning)
- 🔑 **Extranet**: [API & Cloud Dashboard](https://extranet.dlubal.com)

---

## License
This package is proprietary software and requires an **active API Service subscription**. Unauthorized use is prohibited.

