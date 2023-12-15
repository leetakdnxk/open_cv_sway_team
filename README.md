## Performing Feature matching between two images with OpenCV
This project provides an example of performing feature matching between two images using OpenCV and Python. Before the matching process, it visually displays the word "Star" around the matched feature points.
#### Packages Used and Versions:
  1. python (3.7.3)
  2. opencv (4.1.0)
  3. numpy (1.61.4)
#### How to run
  1. GitHub Repository Clone:
  
    git clone https://github.com/leetakdnxk/open_cv_sway_team.git
 2. Add Image Files:

    Add star.jpg and mixedimg.jpg image files to the project folder. The image files should be in a path that the code can read.

3. Run the Code in Python Environment:
   * Open the terminal or command prompt and navigate to the project folder.
   * Execute the following command to run the code:

         python final.code.py
4. Check the Results:

   Once the code execution is complete, a window displaying the visual results of comparing and feature matching the two images will appear.

#### Results:
![결과1,2](https://github.com/leetakdnxk/open_cv_sway_team/assets/144330953/e0b05fd2-587a-4a03-9a80-e5133a034e56)
![결과3](https://github.com/leetakdnxk/open_cv_sway_team/assets/144330953/6825c0b8-e30d-4736-812b-ababc072d0f3)

 #### Key Features
 * Noise Removal:
   * Define a function remove_noise to remove noise from an image using Gaussian blur and morphological operations.
   * Apply the noise removal function to both images.
 * Multiscale Matching:
   * Define a function multiscale_matching that performs multiscale feature matching using the ORB (Oriented FAST and Rotated BRIEF) detector and the BFMatcher.
   * Iterate through different scales and find the best scale with the most matches.
   * Obtain keypoints and matches at the best scale.
 * ORB and BFMatcher:
    * Use the ORB detector and BFMatcher on the original grayscale images.
    * Extract good matches based on a distance ratio.
 * Homography and Perspective Transformation:
    * Find the homography matrix using the good matches.
    * raw the region of interest in the destination image using the homography matrix.
 * Draw Matches:
   * Draw matches between the target image and the mixed image.
 * Text Drawing:
   * Calculate the average position of good matching points in both images.
   * Draw the text "Star" near the average positions of good matches in both images.
             

  












#### Reference:
* <https://bkshin.tistory.com/entry/OpenCV-28-%ED%8A%B9%EC%A7%95-%EB%A7%A4%EC%B9%ADFeature-Matching>
   


 










