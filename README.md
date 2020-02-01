# point-cloud-tools
Tools for converting and modifying point clouds.

## pickledata.py
Converts unlabeled point cloud scans into pickle files for use with PointNet++. Uses as input point cloud scans in .txt form.
The locations of these files are indicated by paths.txt, which contains the paths to the directories where the files are stored. 

## augmented_data.py
Converts unlabeled point cloud scans into pickle files for use with PointNet++. Uses as input point cloud scans in .txt form.
The locations of these files are indicated by paths.txt, which contains the paths to the directories where the files are stored.
Additionally, saves rotated versions of the point cloud to the pickle file to augment the data.

## npydata.py
Converts unlabeled point cloud scans scans into .npy files for use with PointNet. Uses as input point cloud scans in .txt form.
The locations of these files are indicated by paths.txt, which contains the paths to the directories where the files are stored.
Outputs one .npy file for each input .txt file.
