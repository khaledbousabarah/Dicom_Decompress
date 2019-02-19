# Dicom_Decompress

This is a standalone-version of the compressed_dicom submodule of the *dicom2nifti*-Package (https://pypi.org/project/dicom2nifti/) .

Requirements:

* GDCMConv
* Pydicom

## Usage

```python
import dicom_decompresser

file = 'sample.dcm'

dicom_decompresser.run(file)  # Replaces file with uncompressed version
```