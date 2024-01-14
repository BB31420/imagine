# OpenAI Image Generation Wrapper, BB31420, Date: 1/13/24
# Upgrades to write - progress bar for image gen?, prompt saving and load prompts for different style images. Image inpainting/mask maker

import tkinter as tk
import tkinter.messagebox
import customtkinter
from openai import OpenAI
import requests
import os
import datetime
import tkinter.filedialog


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.file_path = None  # Initialize file_path attribute to None
        self.file_path2 = None  # Initialize file_path attribute to None


        # Initialize OpenAI client with API key from file
        self.api_key_file = "openai_api_key.txt"
        self.client = self.initialize_openai_client()

        # Create a label to display image URLs or errors
        self.image_url_label = customtkinter.CTkLabel(self, text="", font=("Arial", 12))
        self.image_url_label.grid(row=7, column=0, padx=20, pady=(20, 10))
   
        # Configure window
        self.title("DALL-E API Interface")
        self.geometry(f"{800}x{580}")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")


        # Logo label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Configure", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Get OpenAI Key 
        self.string_input_button = customtkinter.CTkButton(self.sidebar_frame, text="Setup API Key",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=1, column=0, padx=20, pady=(10, 10))


        # Prompt entry
        self.prompt_entry = customtkinter.CTkTextbox(self, width=30, wrap="word") # Make Text box
        self.prompt_entry.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("DALL·E 3")
        self.tabview.add("DALL·E 2")
        self.tabview.tab("DALL·E 3").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("DALL·E 2").grid_columnconfigure(0, weight=1)
        self.tabview.add("DALL·E 2 Variation")
        self.tabview.add("DALL·E 2 Edit")
        self.tabview.tab("DALL·E 2 Variation").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("DALL·E 2 Edit").grid_columnconfigure(0, weight=1)


        
        # Dall e 3 Image Gen Tab
        
        # Resolution
        self.label_tab_1 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 3"), text="Size")
        self.label_tab_1.grid(row=0, column=0, padx=0, pady=0)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 3"), dynamic_resizing=False,
                                                        values=["1024x1024", "1024x1792 - vertical", "1792x1024 - wider"])
        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(0, 0))

        # Quality
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 3"), text="Quality")
        self.label_tab_2.grid(row=2, column=0, padx=0, pady=0)      
  
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 3"), dynamic_resizing=False,
                                                        values=["hd", "standard"])
        self.optionmenu_2.grid(row=3, column=0, padx=20, pady=(0, 0))

        # Style 
        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 3"), text="Style")
        self.label_tab_3.grid(row=4, column=0, padx=0, pady=0)

        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 3"), dynamic_resizing=False,
                                                        values=["natural", "vivid"])
        self.optionmenu_3.grid(row=5, column=0, padx=0, pady=(0, 0))


        # Generate Dalle3 Image Button
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DALL·E 3"), text="Generate Image",
                                                           command=self.generate_image_dalle3)
        self.string_input_button.grid(row=7, column=0, padx=20, pady=(40, 10))



        # Dall e 2 Image Gen Tab

        # Resolution
        self.label_tab_11 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 2"), text="Size")
        self.label_tab_11.grid(row=0, column=0, padx=0, pady=0)

        self.optionmenu_11 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 2"), dynamic_resizing=False,
                                                        values=["1024x1024", "512x512", "256x256"])
        self.optionmenu_11.grid(row=1, column=0, padx=20, pady=(0, 0))

        # Number of Images
        self.label_tab_22 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 2"), text="Number")
        self.label_tab_22.grid(row=2, column=0, padx=0, pady=0)      
  
        self.optionmenu_22 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 2"), dynamic_resizing=False,
                                                        values=["1", "2", "3", "4", "5"])
        self.optionmenu_22.grid(row=3, column=0, padx=20, pady=(0, 0))

        
        # Generate Dalle2 Image Button
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DALL·E 2"), text="Generate Image",
                                                           command=self.generate_image_dalle2)
        self.string_input_button.grid(row=8, column=0, padx=20, pady=(40, 10))



        # Dall e 2 Variations Tab

        # Resolution
        self.label_tab_111 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 2 Variation"), text="Size")
        self.label_tab_111.grid(row=0, column=0, padx=0, pady=0)

        self.optionmenu_111 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 2 Variation"), dynamic_resizing=False,
                                                        values=["1024x1024", "512x512", "256x256"])
        self.optionmenu_111.grid(row=1, column=0, padx=20, pady=(0, 0))

        # Number of Images
        self.label_tab_222 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 2 Variation"), text="Number")
        self.label_tab_222.grid(row=2, column=0, padx=0, pady=0)      
  
        self.optionmenu_222 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 2 Variation"), dynamic_resizing=False,
                                                        values=["1", "2", "3", "4", "5"])
        self.optionmenu_222.grid(row=3, column=0, padx=20, pady=(0, 0))

        # Upload Image 
        self.select_file_button = customtkinter.CTkButton(self.tabview.tab("DALL·E 2 Variation"), text="Select Image File",
                                                  command=self.select_file_dialog)
        self.select_file_button.grid(row=4, column=0, padx=20, pady=(10, 0))

        
        # Generate Dalle2 Image Button
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DALL·E 2 Variation"), text="Generate Image",
                                                           command=self.generate_image_dalle2_variation)
        self.string_input_button.grid(row=8, column=0, padx=20, pady=(40, 10))
        


        # Dall e 2 Mask Edit Tab

        # Resolution
        self.label_tab_1111 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 2 Edit"), text="Size")
        self.label_tab_1111.grid(row=0, column=0, padx=0, pady=0)

        self.optionmenu_1111 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 2 Edit"), dynamic_resizing=False,
                                                        values=["1024x1024", "512x512", "256x256"])
        self.optionmenu_1111.grid(row=1, column=0, padx=20, pady=(0, 0))

        # Number of Images
        self.label_tab_2222 = customtkinter.CTkLabel(self.tabview.tab("DALL·E 2 Edit"), text="Number")
        self.label_tab_2222.grid(row=2, column=0, padx=0, pady=0)      
  
        self.optionmenu_2222 = customtkinter.CTkOptionMenu(self.tabview.tab("DALL·E 2 Edit"), dynamic_resizing=False,
                                                        values=["1", "2", "3", "4", "5"])
        self.optionmenu_2222.grid(row=3, column=0, padx=20, pady=(0, 0))

        # Upload Image 
        self.select_file_button = customtkinter.CTkButton(self.tabview.tab("DALL·E 2 Edit"), text="Select Image File",
                                                  command=self.select_file_dialog)
        self.select_file_button.grid(row=4, column=0, padx=20, pady=(10, 0))

        # Upload Image Mask 
        self.select_file_button = customtkinter.CTkButton(self.tabview.tab("DALL·E 2 Edit"), text="Select Mask File",
                                                  command=self.select_file_dialog2)
        self.select_file_button.grid(row=5, column=0, padx=20, pady=(10, 0))

        
        # Generate Dalle2 Image Button
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DALL·E 2 Edit"), text="Generate Image",
                                                           command=self.generate_image_dalle2_edit)
        self.string_input_button.grid(row=8, column=0, padx=20, pady=(40, 10))


        # Set default values
        self.prompt_entry.insert("0.0", "Vector logo design of a Greek statue, minimalistic, with a white background")
    
    

    def generate_image_dalle3(self):
        # Get values from input fields
        prompt_text = self.prompt_entry.get("1.0", tk.END).strip()
        size_value = self.optionmenu_1.get()  # Update to get size value
        quality_value = self.optionmenu_2.get()  # Update to get quality value
        
        # Ensure that all required values are present
        if not all([prompt_text, size_value, quality_value]):
            self.image_url_label.configure(text="Please fill in all the required fields.")
            return

        # Make sure the directory exists
        save_dir = "generated_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Make API call to DALL-E 3
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt_text,
                size=size_value,
                quality=quality_value,
            )

            # Check if the response contains data and if it's a list
            if response.data and isinstance(response.data, list):
                image_url = response.data[0].url
                
                # Download the image using the requests library
                image_response = requests.get(image_url)
                
                # Check if the request was successful
            if image_response.status_code == 200:
                # Generate a timestamp string
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                # Create a unique filename with the timestamp
                save_path = f"generated_images/image_{timestamp}.png"

                with open(save_path, 'wb') as image_file:
                    image_file.write(image_response.content)

            # Update the label to indicate successful generation
                self.image_url_label.configure(text="Image successfully generated and saved!")

            else:
                raise ValueError("Failed to download the image.")
        
        except Exception as e:
            self.image_url_label.configure(text=f"Error generating image: {e}")
    


    def generate_image_dalle2(self):
        # Get values from input fields
        prompt_text = self.prompt_entry.get("1.0", tk.END).strip()
        size_value = self.optionmenu_11.get()  # Update to get size value
        number_value = self.optionmenu_22.get()

        # Ensure that all required values are present
        if not all([number_value, size_value, prompt_text]):
            self.image_url_label.configure(text="Please fill in all the required fields.")
            return

        # Make sure the directory exists
        save_dir = "generated_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Make API call to DALL-E 2
        try:
            response = self.client.images.generate(
                prompt=prompt_text,
                model="dall-e-2",
                size=size_value,
                n=int(number_value),
            )

            # Check if the response contains data and if it's a list
            if response.data and isinstance(response.data, list):
                for index, item in enumerate(response.data):
                    image_url = item.url

                    # Download the image using the requests library
                    image_response = requests.get(image_url)
                
                    # Check if the request was successful
                    if image_response.status_code == 200:
                        # Generate a timestamp string for each image
                        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                        # Create a unique filename with the timestamp and index
                        save_path = f"generated_images/image_{timestamp}_{index}.png"

                        with open(save_path, 'wb') as image_file:
                            image_file.write(image_response.content)
                    else:
                        raise ValueError(f"Failed to download image {index + 1}.")
            
                # Update the label to indicate successful generation
                self.image_url_label.configure(text=f"{number_value} images successfully generated and saved!")
            else:
                raise ValueError("No image URLs returned from the API.")

        except Exception as e:
            self.image_url_label.configure(text=f"Error generating images: {e}")



    def generate_image_dalle2_variation(self):
        # Get values from input fields
        size_value = self.optionmenu_111.get()
        number_value = int(self.optionmenu_222.get())  # Convert to integer
        image_value = open(self.file_path, "rb")

        # Ensure that all required values are present
        if not all([size_value, number_value, image_value]):
            self.image_url_label.configure(text="Please fill in all the required fields.")
            return

        # Make sure the directory exists
        save_dir = "generated_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Make API call to DALL-E 2
        try:
            response = self.client.images.create_variation(
                model="dall-e-2",
                size=size_value,
                n=number_value,
                image=image_value,
            )

            # Check if the response contains data and if it's a list
            if response.data and isinstance(response.data, list):
                for index, item in enumerate(response.data):
                    image_url = item.url

                    # Download the image using the requests library
                    image_response = requests.get(image_url)
                
                    # Check if the request was successful
                    if image_response.status_code == 200:
                        # Generate a timestamp string for each image
                        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                        # Create a unique filename with the timestamp and index
                        save_path = f"generated_images/image_{timestamp}_{index}.png"

                        with open(save_path, 'wb') as image_file:
                            image_file.write(image_response.content)
                    else:
                        raise ValueError(f"Failed to download image {index + 1}.")
            
                # Update the label to indicate successful generation
                self.image_url_label.configure(text=f"{number_value} images successfully generated and saved!")
            else:
                raise ValueError("No image URLs returned from the API.")

        except Exception as e:
            self.image_url_label.configure(text=f"Error generating images: {e}")



    def generate_image_dalle2_edit(self):
        # Get values from input fields
        prompt_text = self.prompt_entry.get("1.0", tk.END).strip()
        size_value = self.optionmenu_1111.get()
        number_value = int(self.optionmenu_2222.get())  # Convert to integer
        image_value = open(self.file_path, "rb")
        mask_value = open(self.file_path2, "rb")

        # Ensure that all required values are present
        if not all([size_value, number_value, image_value, mask_value]):
            self.image_url_label.configure(text="Please fill in all the required fields.")
            return

        # Make sure the directory exists
        save_dir = "generated_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Make API call to DALL-E 2
        try:
            response = self.client.images.edit(
                prompt=prompt_text,
                model="dall-e-2",
                size=size_value,
                n=number_value,
                image=image_value,
                mask=mask_value,
            )

            # Check if the response contains data and if it's a list
            if response.data and isinstance(response.data, list):
                for index, item in enumerate(response.data):
                    image_url = item.url

                    # Download the image using the requests library
                    image_response = requests.get(image_url)
                
                    # Check if the request was successful
                    if image_response.status_code == 200:
                        # Generate a timestamp string for each image
                        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                        # Create a unique filename with the timestamp and index
                        save_path = f"generated_images/image_{timestamp}_{index}.png"

                        with open(save_path, 'wb') as image_file:
                            image_file.write(image_response.content)
                    else:
                        raise ValueError(f"Failed to download image {index + 1}.")
            
                # Update the label to indicate successful generation
                self.image_url_label.configure(text=f"{number_value} images successfully generated and saved!")
            else:
                raise ValueError("No image URLs returned from the API.")

        except Exception as e:
            self.image_url_label.configure(text=f"Error generating images: {e}")        



    def initialize_openai_client(self):
        # Check if the API key file exists
        if os.path.exists(self.api_key_file):
            with open(self.api_key_file, "r") as f:
                api_key = f.read().strip()
                if api_key:
                    return OpenAI(api_key=api_key)
        
        # If file doesn't exist or API key is not valid, return None
        return None    


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in OpenAi API key:", title="Save OpenAi API Key")
        api_key = dialog.get_input()
        
        # Save the API key to a file
        if api_key:
            with open(self.api_key_file, "w") as f:
                f.write(api_key)


    def select_file_dialog(self):
        self.file_path = tkinter.filedialog.askopenfilename(title="Select an Image File")
        if self.file_path:
            print(f"Selected file: {self.file_path}")

    def select_file_dialog2(self):
        self.file_path2 = tkinter.filedialog.askopenfilename(title="Select an Image File")
        if self.file_path2:
            print(f"Selected file: {self.file_path2}")

        

if __name__ == "__main__":
    app = App()
    app.mainloop()