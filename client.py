import base64
import streamlit as st
import requests
from uuid import uuid4
from io import BytesIO
from PIL import Image

BASE_URL = "http://localhost:8000"  # Adjust if necessary

# pip install streamlit
# to start the client run
# streamlit run client.py


# Helper function to display a small image (thumbnail)
def display_thumbnail(base64_string):
    image_data = base64.b64decode(base64_string) # Decode Base64 string into bytes
    image = Image.open(BytesIO(image_data))
    image.thumbnail((128, 128))  # Resize image to a thumbnail
    return image


def create_user_form():
    # TODO: use st.form to create a form for user creation
    with st.form("create_user_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        graduated = st.checkbox("Graduated")
        submit_button = st.form_submit_button("Create User")
# TODO: if form was submitted, then make a post request to create a user
        if submit_button:
            response = requests.post(f"{BASE_URL}/user/", json={"name": name, "age": age, "graduated": graduated})
            if response.status_code == 201:
                st.success("User created successfully!")
            else:
                st.error(f"Failed to create user: {response.text}")   
    


def set_profile_pic():
    # Store user input in session state
    if "user_id" not in st.session_state:
        st.session_state.user_id = ""

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    # User ID Input
    user_id = st.text_input(
        "Enter User ID", value=st.session_state.user_id, placeholder="Enter User ID"
    )
    if user_id:
        st.session_state.user_id = user_id.strip()  # Store value when entered

    # File Uploader
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file  # Store file when uploaded

    # Upload Button
    upload_button = st.button("Upload Picture")

    # Ensure all fields are set before sending the request
    if upload_button and st.session_state.user_id and st.session_state.uploaded_file:
        files = {
            "file": (
                st.session_state.uploaded_file.name,
                st.session_state.uploaded_file,
                st.session_state.uploaded_file.type,
            )
        }

        # TODO: send a file and use success/error to handle status code
        if response.status_code == 200:
            st.success("Profile picture uploaded successfully!")
        else:
            st.error("Failed to upload profile picture.")

    elif upload_button:
        st.warning(
            "Please provide both User ID and a Profile Picture before uploading."
        )


def display_user(user):
    with st.expander(f"User: {user['name']}"):
        cols = st.columns(
            [1, 4]
        )  # Thumbnail in small column, user info in larger column
        with cols[0]:  # First column (small) for profile picture
            if user.get("profile_picture"):
                st.image(display_thumbnail(user["profile_picture"]))
            else:
                st.write("No Image")
        with cols[1]:  # Second column for user details
            # Editable fields
            new_name = st.text_input(
                f"Edit Name", value=user["name"], key=f"name_{user['id']}"
            )
            new_age = st.number_input(
                f"Edit Age", min_value=0, value=user["age"], key=f"age_{user['id']}"
            )
            new_graduated = st.checkbox(
                f"Graduated", value=user["graduated"], key=f"grad_{user['id']}"
            )
            st.write(f"ID: {user['id']}")
            # Update button
            if st.button(f"Update {user['name']}", key=f"update_{user['id']}"):
                update_data = {
                    "name": new_name,
                    "age": new_age,
                    "graduated": new_graduated,
                }

                # TODO: update user and handle status_code
                response = requests.put(f"{BASE_URL}/user/{user['id']}", json=update_data)
                if response.status_code == 200:
                    st.success("User updated successfully!")
                else:
                    st.error(f"Failed to update user: {response.text}")


def display_all_users(response):
    users = response.json()
    for user in users:
        display_user(user)


if __name__ == "__main__":
    st.title("User Management with FastAPI")

    # Create User Form
    st.header("Create New User")
    create_user_form()

    # Set Profile Picture
    st.header("Set Profile Picture")
    set_profile_pic()

    # Display All Users with Edit Option
    st.header("All Users")
    response = requests.get(f"{BASE_URL}/user/")
    if response.status_code == 200:
        display_all_users(response)
    else:
        st.error("Failed to retrieve users.")
