from oriansoft.src.functions import choose_file

from pyscript import document

choose_file_btn = document.getElementById("choose_file_btn")

if choose_file_btn is not None:
    choose_file_btn.addEventListener("click", choose_file)
