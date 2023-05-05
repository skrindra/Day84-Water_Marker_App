from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os


# ----------- CONSTANTS ----------------------
BG_COLOR = "khaki"
COLOR_OPTIONS = ["white", "red", "black", "blue"]
POSITIONS = ["Bottom-Right", "Top-Left", "Top-Right", "Bottom-Left"]


# --------- The App Functionality ---------
class WatermarkApp:
    def __init__(self, master):
        # master is the incoming root window
        self.master = master
        self.master.title("Watermark App")
        self.master.geometry("800x1000")
        self.master.config(background=BG_COLOR)

        # ----------- CREATING THE WIDGETS---------#
        # ----The Header Widget-----
        self.header_canvas = Canvas(master, width=800, height=200)
        self.header_image = Image.open("sky_image.jpeg")  # replace with your own image file
        self.header_image = self.header_image.resize((800, 200))
        self.header_bg = ImageTk.PhotoImage(self.header_image)
        self.header_canvas.create_image(0, 0, anchor=NW, image=self.header_bg)

        # ----Other widgets ------
        self.header_label = Label(master, text="ZinGo Marker App", bg=BG_COLOR, font=("Arial", 40))
        self.canvas = Canvas(master, width=470, height=560, bg="green")

        self.upload_button = Button(master,
                                    text="Upload Image",
                                    highlightthickness=0,
                                    highlightbackground="blue",
                                    command=self.upload_image
                                    )

        self.watermark_button = Button(master,
                                       text="Add Watermark",
                                       command=self.add_watermark,
                                       highlightthickness=0,
                                       highlightbackground="blue"
                                       )

        self.download_button = Button(master,
                                      text="Download Image",
                                      highlightbackground="red",
                                      highlightthickness=0,
                                      command=self.download_image
                                      )

        # -------- PERSONALIZATION WIDGETS---------
        # ------[ Water mark text ]-------
        self.watermark_text_label = Label(master, text="Enter the Watermark Text:", bg=BG_COLOR)
        self.watermark_text_entry = Entry(master)

        # ------[ Text color selection ]-------
        self.text_color = None
        # storing the selected option
        self.selected_color = StringVar()
        # setting the default color as option 1
        self.selected_color.set(COLOR_OPTIONS[0])
        self.watermark_color_label = Label(master, text="Choose a text color:", bg=BG_COLOR)
        # Create a dropdown menu widget using selected option and all options
        self.colors_dropdown = OptionMenu(master, self.selected_color, *COLOR_OPTIONS)

        # Create a button to call the 'color_selected' function
        self.color_select_button = Button(master, text="Select", command=self.color_selected, highlightthickness=0)

        # ------[ Text Position selection ]-------
        self.text_position = None
        # storing the selected option
        self.selected_position = StringVar()
        # setting the default position as bottom-right
        self.selected_position.set(POSITIONS[0])
        self.position_label = Label(master, text="Select a Text Position:", bg=BG_COLOR)
        # Create a dropdown menu widget using selected option and all options
        self.positions_dropdown = OptionMenu(master, self.selected_position, *POSITIONS)

        # Create a button to call the 'position_selected' function
        self.position_select_button = Button(master,
                                             text="Select",
                                             command=self.position_selected,
                                             highlightthickness=0)

        # ----- CLEAR THE WATERMARK ------- #
        self.clear_watermark_button = Button(master,
                                             text="Clear Watermark",
                                             command=self.delete_watermark,
                                             highlightthickness=0,
                                             highlightbackground="blue")

        # -------- PACKING / POSITIONING THE WIDGETS-----------#
        self.header_canvas.place(x=0, y=0)
        self.header_label.place(x=270, y=30)
        self.canvas.place(x=10, y=150)
        self.upload_button.place(x=500, y=160)
        self.watermark_text_label.place(x=500, y=200)
        self.watermark_text_entry.place(x=500, y=225)

        self.watermark_color_label.place(x=500, y=260)
        self.colors_dropdown.place(x=500, y=290)
        self.color_select_button.place(x=600, y=288)

        self.position_label.place(x=500, y=330)
        self.positions_dropdown.place(x=500, y=360)
        self.position_select_button.place(x=640, y=358)

        self.watermark_button.place(x=500, y=430)
        self.clear_watermark_button.place(x=640, y=430)
        self.download_button.place(x=500, y=460)

        # ----- INITIALIZING THE VARIABLES ------
        self.image_path = None
        self.image = None  # (This image will become the drawing object)
        self.original_image = None  # (Storing a copy of original image)
        self.watermarked_image = None  # (The final watermarked image)
        self.canvas_image = None  # (Tk inter compatible image)

    def color_selected(self):
        # update the selected color variable
        self.text_color = self.selected_color.get()

    def position_selected(self):
        # update the selected position variable
        self.text_position = self.selected_position.get()

    def upload_image(self):
        """uploads a user selected image to screen"""
        # Get the path of the image file
        self.image_path = filedialog.askopenfilename(title="Select an Image")
        # Load the image and display it on the canvas
        self.image = Image.open(self.image_path)
        self.original_image = Image.open(self.image_path)
        image_to_show = self.image.resize((450, 550))
        self.canvas_image = ImageTk.PhotoImage(image_to_show)
        padding_x, padding_y = 12, 8
        self.canvas.create_image(padding_x, padding_y, anchor=NW, image=self.canvas_image)

    def add_watermark(self):
        """Adds watermark to the image"""
        if self.image_path is not None:
            # Create a drawing object and define the watermark text and font
            draw = ImageDraw.Draw(self.image)

            # getting the user text
            watermark_text = self.watermark_text_entry.get()

            # FONT STYLE & SIZE CUSTOMIZABLE
            font = ImageFont.truetype("arial.ttf", 50)

            # Calculate the bounding box of the text
            text_bbox = draw.textbbox((0, 0), watermark_text, font)

            # Calculate the size of the text
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate the position of the text (based on selected position)
            position = self.get_position(text_width, text_height)
            x, y = position[0], position[1]

            # Draw the text on the image (This line makes the self.image the watermarked image)
            draw.text((x, y), watermark_text, font=font, fill=self.text_color)

            # Update the canvas with the watermarked image
            self.canvas.delete("all")
            self.watermarked_image = self.image.copy()
            image_to_show = self.watermarked_image.resize((450, 550))
            self.canvas_image = ImageTk.PhotoImage(image_to_show)
            padding_x, padding_y = 12, 8
            self.canvas.create_image(padding_x, padding_y, anchor=NW, image=self.canvas_image)
            # replace the self.image to original
            self.image = self.original_image
            # clear the text box after adding
            self.watermark_text_entry.delete("0", "end")

        else:
            messagebox.showwarning("Warning", "Please upload an image first.")

    def get_position(self, text_width, text_height):
        """Gets the coordinates for the user selected position. Input Arguments: textbox width and height"""
        x = 0
        y = 0
        if self.text_position == "Bottom-Right":
            x = self.image.width - text_width - 25
            y = self.image.height - text_height - 25
        elif self.text_position == "Bottom-Left":
            x = 25
            y = self.image.height - text_height - 25
        elif self.text_position == "Top-Left":
            x = 25
            y = 25
        else:
            x = self.image.width - text_width - 25
            y = 25

        position = (x, y)
        return position

    def delete_watermark(self):
        """deletes the existing watermarked Image and displays the original image"""
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.canvas.delete("all")
            image_to_show = self.image.resize((450, 550))
            self.canvas_image = ImageTk.PhotoImage(image_to_show)
            padding_x, padding_y = 12, 8
            self.canvas.create_image(padding_x, padding_y, anchor=NW, image=self.canvas_image)
        else:
            messagebox.showwarning("Warning", "Please upload an image first.")

    def download_image(self):
        """downloads the watermark image"""
        if self.watermarked_image is not None:
            # Get the file name for the watermarked image
            file_name = filedialog.asksaveasfilename(defaultextension=".png")

            # Save the watermarked image
            self.watermarked_image.save(file_name, "PNG")

            # Show a message box with the file path
            message = "The watermarked image has been saved at:\n" + os.path.abspath(file_name)
            messagebox.showinfo(title="Image Saved", message=message)
        else:
            messagebox.showwarning("Warning", "Please upload an image first.")


# Create the Tkinter window and run the app
root = Tk()
app = WatermarkApp(root)
root.mainloop()
