# OpenDrift tutorial notebooks

## Description
This repository contains jupyter notebooks and python scripts adapted (and inspired) from official [OpenDrift documentation](https://opendrift.github.io/gallery) for demonstrations at EDITO's Platform.

## Content

### Tutorials
Notebooks adapted from [OpenDrift Gallery](https://opendrift.github.io/gallery):
- The [ShipDrift example](./notebooks/tutorials/example_shipdrift.ipynb) is an adapted version from [https://opendrift.github.io/gallery/example_shipdrift.html](https://opendrift.github.io/gallery/example_shipdrift.html)
- The [OpenBerg example](./notebooks/tutorials/example_openberg.ipynb) is an adapted version from [https://opendrift.github.io/gallery/example_openberg.html](https://opendrift.github.io/gallery/example_openberg.html)
- The [Drift at Different Depths example](./notebooks/tutorials/example_depth.ipynb) is an adapted version from [https://opendrift.github.io/gallery/example_depth.html]

### Demos
Notebooks for EDITO, WeKEO, and Marine Data Store:

- [An OpenDrift comparison over different products of Copernicus Marine Data Store](./notebooks/demos/opendrift_demo.ipynb), provides a set of simulations at the North-west shelves MFC by accessing Copernicus Marine Global Data Store. These simulations use data from MDS and TOPAZ6, and their results are compared through the drift trajectory of a set of Lagrangian particles for each dataset.

- The notebook [OpenBerg for UNOC3.ipynb](./notebooks/demos/OpenBerg_for_UNOC3.ipynb), is a tutorial presented at UNOC3 to select and track an iceberg from Copernicus Marine Datastore service. This tutorial provides a simulation that uses data from MDS and TOPAZ6, and its results are compared through the drift trajectory of a set of Lagrangian particles for each dataset.

- The notebook [OpenBerg presented at Copernicus Hubs Essentials.ipynb](./notebooks/demos/OpenBerg_presented_at_Copernicus_Hubs_Essentials.ipynb), is a tutorial presented at [Copernicus hub essentials](https://events.coastal.hub.copernicus.eu/e/copernicus-hubs-essentials) to select and track an iceberg from Copernicus Marine Datastore service. In this tutorial, we explore the tip depth icebergs’ role on possible trajectories. We compute a Lagrangian simulation using data from MDS for a set of different iceberg tip depths. We consider the vertical oceanic currents profile and compare the results with a simulation taking into account the surface currents.

- The ["Tracking and simulating Iceberg Juliette's faith" notebook](./notebooks/demos/OpenBerg_for_DOF.ipynb) for a demonstration of simulating track of [Iceberg Juliette](https://nersc.no/en/features/juliette-helps-us-produce-better-forecasts/) with OpenBerg and shown at Digital Ocean Forum 2025

## Installing and running

> [!IMPORTANT]  
> Some notebooks might require Copernicus Marine credentials. 
> To configure your credentials in EDITO's platform refer to [Providing secrets section](#providing-secrets)
> Otherwise, you might refer to [https://help.marine.copernicus.eu/en/articles/8185007-copernicus-marine-toolbox-credentials-configuration](https://help.marine.copernicus.eu/en/articles/8185007-copernicus-marine-toolbox-credentials-configuration))

These notebooks were published for being run on EDITO's platform. Still, as any other jupyter notebook, you'd be able to run them from any other jupyterhub session (local or remote). If you want to execute these notebooks in any other environement but EDITO's, go to [Running on another environment section](#running-on-another-environment).


### Running the service at EDITO Datalab

> [!TIP]  
> For further information about EDITO's platform and the DataLab, please go to [EDITO's Platform Overview](https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/PlatformOverview/platform-videos).

OpenDrift can be lauched using an [autolauch function from Datalab's Service catalog](https://datalab.dive.edito.eu/launcher/service-playground/jupyter-python-opendrift?name=jupyter-python-opendrift&shared=false&version=1.0.4&s3=region-7e02ff37&resources.requests.cpu=«1200m»&resources.requests.memory=«4Gi»&resources.limits.cpu=«7200m»&resources.limits.memory=«28Gi»&vault.secret=«copernicus-marine»&autoLaunch=true) as it is described at the _*"Run OpenDrift"*_ tutorial panel under [the EDITO Ocean Modelling tutorials section](https://dive.edito.eu/training?search=ACCIBERG).

#### Set of instructions to open OpenDrift in EDITO's platform:

First lauch EDITO's platform accesible from: [https://datalab.dive.edito.eu/](https://datalab.dive.edito.eu/), you must get a screen as:
<img src="images/01-EDITO_LogIn.png" alt="drawing" width="700"/>

Log in and register if needed,

<img src="images/02-EDITO_LogIn.png" alt="drawing" width="700"/>

after logging-in you'd have a screen as:

<img src="images/03-EDITO_LoggedIn.png" alt="drawing" width="700"/>

In here, you can launch your desired service, OpenDrift, by serching for it in the service catalog.

<img src="images/04-EDITO_Service_catalog.png" alt="drawing" width="300"/>
<img src="images/05-EDITO_Research.png" alt="drawing" width="400"/>

you must get something like,

<img src="images/06-EDITO_Result.png" alt="drawing" width="300"/>

click on the LAUNCH buttom to have:

<img src="images/07-EDITO_Launcher.png" alt="drawing" width="700"/>

#### Providing secrets
To provide your secrets through application, EDITO Datalab uses a dedicated secret manager - _*Vault*_ - customizable from the _*"My Secrets"*_ section (see the [Managing secrets page](https://dive.edito.eu/training?search=Managing%20secrets) for further details)


From there, you may define environment variables that will be readable from your applications.

For Copernicus Marine, as explained in [copernicus marine toolbox site](https://help.marine.copernicus.eu/en/articles/7970514-copernicus-marine-toolbox-installation), you will need to set the `COPERNICUSMARINE_SERVICE_USERNAME` and `COPERNICUSMARINE_SERVICE_PASSWORD` variables with your credentials

Go to your left hand side menu and select the option _*"MySecrets"*_,

<img src="images/19-EDITO_MySecrets.png" alt="drawing" width="100"/>

Once you open it, go to the top menu and select the option _*"Create a new secret"*_

<img src="images/20-EDITO_NewSecret.png" alt="drawing" width="300"/>

then you'll have a <img src="images/21-EDITO_Rename_your_secret.png" alt="drawing" width="50"/> rename it, as we're using copernicusmarine set of passwords. I name it like that, <img src="images/22-EDITO_CopernicusMarine_Secret.png" alt="drawing" width="50"/>. 

Open it and _*"Add a new variable"*_

<img src="images/23_EDITO_CopernicusMarine_newVar.png" alt="drawing" width="300"/>

to set the value, don't forget to click on the check icon:

<img src="images/24-EDITO_CopernicusMarine_SetUser.png" alt="drawing" width="300"/>

Once you're done, click on _*"Use in services"*_ botton,

<img src="images/25_EDITO_CopernicusMarine_setSecret.png" alt="drawing" width="300"/>
<img src="images/26_EDITO_Pop-up.png" alt="drawing" width="300"/>

Once done, the notebook application has to be informed of where to find these secrets, through the _*"Vault"*_ tab before launching the application. Provide in this tab the values that correspond to the directory (usually username) and path where secret variables are defined.

<img src="images/08-EDITO_Vault.png" alt="drawing" width="700"/>

#### Available resources to launch an EDITO's service

If you're already done it, you can also set the available resources for your configuration, like the quantity of processors (units in milli-CPU, thus 1000m means 1 CPU)

<img src="images/09-EDITO_SelectResources.png" alt="drawing" width="700"/>

<img src="images/10-EDITO_SelectResources.png" alt="drawing" width="700"/>

#### Save a configuration
In order to avoid selecting all the time your available resources and/or setting your vault configuration, you can save your service configuration.

<img src="images/11-EDITO-SaveConfig.png" alt="drawing" width="700"/>

By doing so, your configuration setup is going to be saved to the MyServices section,

<img src="images/12-EDITO_MyServices.png" alt="drawing" width="150"/>

where you can simply launch it, and you'll have your previous configuration.

<img src="images/13-EDITO_Launch.png" alt="drawing" width="500"/>

<img src="images/14-EDITO_Launch_from_saved.png" alt="drawing" width="700"/>

#### Once launched, what to expect,
If everything goes ok, you'll get a screen like this. It will take a few seconds/minutes, depending on the requested configuration, to load your service. Once you're done the copy-password screen will appear.

<img src="images/15-EDITO_Loading.png" alt="drawing" width="700"/>

Copy your password,

<img src="images/16-EDITO_CopyPassword.png" alt="drawing" width="300"/>

Click into the open service button

<img src="images/17-EDITO_OpenService.png" alt="drawing" width="300"/>

and finally paste the password copied on your clipboard to,

<img src="images/18-EDITO_Paste-pwd.png" alt="drawing" width="300"/>

#### Setting your own EDITO environment

You may want to run these notebooks from a blank Jupyterlab session. To do that, you will need to 1) init the session environment, 2) clone the repository content in the session.

To do so, the [following URL](https://datalab.dive.edito.eu/launcher/ide/jupyter-python?name=jupyter-python&autoLaunch=true&service.image.version=«inseefrlab%2Fonyxia-jupyter-python%3Apy3.11.10»&init.personalInit=«https%3A%2F%2Fgitlab.mercator-ocean.fr%2Fpub%2Fedito-model-lab%2Ftutorials%2F-%2Fraw%2Fmaster%2Fsources%2FOpenDrift%2Fscripts%2Finit.sh») will launch a blank jupyter-python session and running
a specific [`init.sh`](./scripts/init.sh) script that will do that for you.

### Running on another environment

For running the notebooks on an environment of your choice, you will need to clone this repository to your JupyterLab session.
For that, you may directly use the Clone repository function from the [JupyterLab Git extension](https://github.com/jupyterlab/jupyterlab-git).

## Contributing to the repository

Developer contributions would be happily merged into the code base through a Merge Request. To get granted permissions to contribute to the project, please contact Mercator.

