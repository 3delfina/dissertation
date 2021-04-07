# Implementation of a Tool for DeepFake Obfuscation
This is the implementation part of the Level 5 MSci dissertation project "Implementation and Evaluation of a Tool for DeepFake Obfuscation".

We built a web application called Photo Obfuscator that allows users to upload photos and apply different obfuscation techniques such as blurring, pixelating, masking, DeepFake and avatar (emoji) to the faces of owners and non-owners of the photos.  The evaluation of the obfuscation techniques was performed by conducting two within-subjects experiments - an online user study and a questionnaire.

The web application is currently deployed to http://mkhamis.pythonanywhere.com/.

## Installation
### Cloning the project and creating a virtual environment
    git clone https://github.com/3delfina/dissertation.git
    mkvirtualenv --python=/usr/bin/python3.6
    python3 -m venv venv
    source venv/bin/activate
### Installing the dependencies (since some of them need additional flags, we install them separately)
    cd dissertation/
    pip install -r requirements.txt
    pip install https://download.pytorch.org/whl/cpu/torch-1.7.1%2Bcpu-cp36-cp36m-linux_x86_64.whl
    pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
    pip install Django==3.1.2
    pip install imutils==0.5.3
    pip install opencv-python-headless==4.2.0.32
    pip install matplotlib==3.3.3
    pip install tensorboard==2.4.0
    pip install addict==2.4.0
    pip install face-detection==0.2.1
    pip install albumentations==0.5.2
    pip install whitenoise==5.2.0
    pip install tqdm
    pip install scikit-image==0.17.2
### Migrating  
    python manage.py migrate
    python manage.py migrate
### Starting the server locally
	python manage.py runserver

## Usage
On the landing page, the user is invited to upload a photo and apply different obfuscation techniques on the faces to protect their privacy. The form on the landing page is pre-filled with the participant id, generated by calculating the Unix timestamp in milliseconds. The only other field required is the participant photo. Once the user uploads a photo, it gets processed in the background to locate face coordinates and create a DeepFake of all of the faces, and the user is redirected to a different page. The redirection step takes around 20 seconds due to the costly process of creating a DeepFake, so the user is shown a GIF image with the text asking them to wait.

Once redirected to a different page, the user is able to see their id and the filename of the photo uploaded, along with the original photo with all of the faces located and numbered. The user has an option to complete a form and pick numbers corresponding to the faces they wish to obfuscate or to upload a different photo. In case when the user selects the faces and clicks “Obfuscate selected”, the page is updated with 6 buttons, clicking on which displays the photos with one of the following obfuscation techniques applied: original (no obfuscation), blurring, pixelating, masking, DeepFake and avatar (emoji). The user may change the selection of faces at any point by using the aforementioned “Obfuscate selected” button.

## DeepFake implementation
For the original implementation of the DeepFake generator please refer to https://github.com/hukkelas/DeepPrivacy.
The version that was used and modified for this project corresponds to the commit de30f54 (full id de30f547428277385db6b0536c9b74750f56e1eb) on 5 Jan 2021.
