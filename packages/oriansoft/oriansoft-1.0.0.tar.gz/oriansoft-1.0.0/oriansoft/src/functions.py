from pyscript import document


def choose_file(e):
    file_input = document.getElementById("image_tools_file")
    file_input.click()
