#### Introduction
The XML Management Interface is a powerful way to configure and administer the Datapower appliance. SOMA (SOAP Configuration Management) scripts are one way to use XMI. This example shows how you can create a sample SOMA script using Python to add multiple WSDL files to a WSP using the XMI.

#### Prerequisites
1. Python 3.7.5 or higher installed.
    
    For Windows look [here](https://www.python.org/downloads/windows/). Check version with `py --version`

    For Mac look [here](https://www.python.org/downloads/mac-osx/). Python comes preinstalled with all new Macs. Check `python3 --version` in terminal before downloading.
2. XML Management Interface is enabled for Datapower appliance for SOMA to work.
    See [here](https://www.ibm.com/support/knowledgecenter/en/SS9H2Y_7.7.0/com.ibm.dp.doc/xmi_interfaceservices_enabling.html) how to find that out.
    
#### Usage
1. Clone the repository
2. Install required Python modules.

    For Windows: `py -m pip install -r requirements.txt`
    
    For Mac: `pip3 install -r requirements.txt`
3. [Optional] Create a Python Virtual Environment.

    I only know how to do this in Mac; but I'm sure windows commands are very similar.
    * Install: `pip3 install virtualenv`
    * Create new: `python3 -m venv env`
    * Activate: `source env/bin/activate`
    * Verify: `which python` - should show you a path similar to /directory/env
    * Once done, Deactivate: `deactivate`
    
4. Run script.

    For Windows: `py main.py --help`. Prompt will show you all available options and defaults.
    
    For Mac: `python3 main.py --help`. Prompt will show you all available options and defaults.
    
5. Output will be the SOMA xml file that you require to run against your Datapower appliance in `./output` directory.

6. To run the SOMA file use command `curl –k –u user:password –d @SOMA.xml https://DataPowerIP:Port/EndpointURI`
