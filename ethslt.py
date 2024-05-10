import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageTk
import threading
import cv2
import mediapipe as mp

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image, results
def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                              mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                              mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))

    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("ETHSLT")
        self.root.iconbitmap("icon.ico")

        # Load image
        self.image = Image.open("Image/logo1.png")
        self.photo = ImageTk.PhotoImage(self.image)

        # Add image to label
        self.image_label = ttk.Label(root, image=self.photo)
        self.image_label.place(x=0, y=0, relwidth=0.7, relheight=1)  # Adjusted width

        # Add label
        self.label = ttk.Label(root, text="                  ETHSLT \n\n የምልክት ቋንቋ ወደ ጽሑፍ መቀየሪያ ", font=("Helvetica", 24))
        self.label.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

        # Create a label to display the camera preview
        self.label_camera_preview = tk.Label(root)
        self.label_camera_preview.place(relx=0.7, rely=0.4, anchor=tk.CENTER)  # New placement for camera preview

        # Add button
        self.button = ttk.Button(root, text="         መተርጎም ጀምር         ", command=self.start_camera)
        self.button.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

        # Create a progress bar for loading animation
        self.progressbar = ttk.Progressbar(root, mode="indeterminate")

        # Variable to store the camera state
        self.camera_active = False

        # Center the window
        self.center_window()

    def start_camera(self):
        if not self.camera_active:
            # Show loading animation
            self.progressbar.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
            self.progressbar.start()

            # Start camera initialization in a new thread
            self.camera_thread = threading.Thread(target=self.initialize_camera)
            self.camera_thread.start()

    def initialize_camera(self):
        # Open camera in a separate thread
        self.cap = cv2.VideoCapture(0)

        # Check if camera is opened successfully
        if self.cap.isOpened():
            # Stop loading animation
            self.progressbar.stop()
            self.progressbar.place_forget()

            # Set camera state to active
            self.camera_active = True

            # Start camera preview
            self.camera_preview(self.cap)
        else:
            # Stop loading animation if camera failed to open
            self.progressbar.stop()
            self.progressbar.place_forget()

            # Inform user about the failure
            print("Failed to open the camera.")

    def camera_preview(self, cap):
        # Set the font and scale for the text
        font_scale = 1
        font_color = (0, 255, 0)
        thickness = 4

        # Set the font path
        font_path = 'font/AbyssinicaSIL-Regular.ttf'
        font = ImageFont.truetype(font_path, 32)

        # Set mediapipe model
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while self.camera_active and cap.isOpened():
                ret, frame = cap.read()

                # make detection
                image, results = mediapipe_detection(frame, holistic)
                # draw landmarks
                draw_styled_landmarks(image, results)

                # Draw Amharic text on the frame
                img_pil = Image.fromarray(image)
                draw = ImageDraw.Draw(img_pil)
                draw.text((10, 20), 'ሰላም እንዴት ናችሁ?', font=font, fill=font_color)
                image = np.array(img_pil)

                # Convert the image to a format compatible with Tkinter
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                photo = ImageTk.PhotoImage(image=image)

                # Display the frame in the Tkinter window
                self.label_camera_preview.config(image=photo)
                self.label_camera_preview.image = photo  # Keep a reference to prevent garbage collection

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

    def center_window(self):
        # Maximize the window
        self.root.state('zoomed')

        # Enable resizing the window
        self.root.resizable(True, True)

# Create and run the splash screen
def main():
    root = tk.Tk()
    app = SplashScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
