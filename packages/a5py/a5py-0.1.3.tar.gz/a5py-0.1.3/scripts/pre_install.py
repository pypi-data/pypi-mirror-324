import subprocess

def get_gdal_version():
    result = subprocess.run(["gdalinfo", "--version"], stdout=subprocess.PIPE, text=True)
    return result.stdout.split()[1].rstrip(",")  # Extract version (e.g., "3.8.4")

def pre_install():
    try:
        # Use GDAL version in a pip command
        gdal_version = get_gdal_version()
        subprocess.run(["pip", "install", f"gdal=={gdal_version}"])
        # create_ini_from_dict(config_data, config_path)
        print(f"GDAL Version Detected: {gdal_version}")
    except Exception as e:
        raise RuntimeError(f"Error detecting GDAL version: {e}")

pre_install()