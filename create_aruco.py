import cv2
import cv2.aruco as aruco
import argparse
import numpy as np
import os


def make_dir(whatever):
    try:
        os.makedirs(whatever)
    except OSError:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Aruco tags in pdf pages')
    parser.add_argument('--num', type=int, required=None, default=2,
                        help='Integer for the amount of tags to generate. Default [2]')

    args = parser.parse_args()
    tag_num = args.num

    # Make folder for models
    make_dir("models")

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    for i in range(0,tag_num):

        # Make folders for tags models
        make_dir("models/tag_"+str(i)+"/materials/textures")
        make_dir("models/tag_"+str(i)+"/materials/scripts")
        

        # ----------Generate tag image----------
        # Last parameter is total image size
        img = aruco.drawMarker(aruco_dict, i, 900)
        image = np.zeros((900, 900, 1), np.uint8)
        image[:] = (0)
        image = cv2.addWeighted( image, 0.9, img, 0.9, 0.0);

        # Border parameter
        top = 50
        bottom = 50
        left = 50
        right = 50
        borderType = cv2.BORDER_CONSTANT
        value = [255,255,255]
        dst = cv2.copyMakeBorder(image, top, bottom, left, right, \
                borderType, None, value)
        
        cv2.imwrite("models/tag_"+str(i)+"/materials/textures/aruco_marker_"+str(i)+".png", dst)
        
        # ----------Generate tag material script----------
        file = open("models/tag_"+str(i)+"/materials/scripts/tag.material", 'w')

        file.write("\n \
material aruco_tag_"+str(i)+"\n \
{\n \
    technique\n \
    {\n \
    pass\n \
    {\n \
        texture_unit\n \
        {\n \
        // Relative to the location of the material script\n \
        texture ../textures/aruco_marker_"+str(i)+".png\n \
        // Repeat the texture over the surface (4 per face)\n \
        scale 1 1\n \
        }\n \
    }\n \
    }\n \
}\n")
        file.close()

        # ----------Generate tag config----------
        file = open("models/tag_"+str(i)+"/model.config", 'w')
        file.write("\n \
<?xml version=\"1.0\"?>\n \
\n \
<model>\n \
  <name>Aruco tag"+ str(i) +"</name>\n \
  <version>1.0</version>\n \
  <sdf version=\"1.6\">model.sdf</sdf>\n \
\n \
  <author>\n \
    <name>Nievas Martin</name>\n \
    <email>martin.nievas.ar@gmail.com</email>\n \
  </author>\n \
\n \
  <description>\n \
  Aruco tag "+str(i)+"\n \
  </description>\n \
\n \
</model>\n \
        ")
        file.close()

        file = open("models/tag_"+str(i)+"/model.sdf", 'w')
        file.write("\n \
<?xml version=\"1.0\"?>\n \
<sdf version=\"1.6\">\n \
  <model name=\"Aruco tag"+ str(i) + "\">\n \
    <static>true</static>\n \
    <link name=\"robot_link\">\n \
      <visual name=\"body_visual\">\n \
        <geometry>\n \
          <box>\n \
            <size>0.3 0.3 0.01</size>\n \
          </box>\n \
        </geometry>\n \
        <material> <!-- Body material -->\n \
          <script>\n \
            <uri>model://tag_"+str(i)+"/materials/scripts/tag.material</uri>\n \
            <name>aruco_tag_"+str(i)+"</name>\n \
          </script>\n \
        </material> <!-- End Body Material -->\n \
      </visual>\n \
    </link>\n \
  </model>\n \
</sdf>\n \
\n")
        file.close()






