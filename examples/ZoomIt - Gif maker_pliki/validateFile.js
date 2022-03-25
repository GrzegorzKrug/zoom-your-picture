ValidateFileIfImage = () => {
    const fiElement = document.getElementById('upImage');
    var button = document.getElementById("submitBt");
    var textField = document.getElementById("validationTextField");
        // Check if any file is selected.
    const allowed_images = ["image/jpeg", "image/jpg", "image/png"]
    if (fiElement.files.length > 0) {
        const file = fiElement.files.item(0);
        const size = Math.round((file.size / 1024));
        const name = file.name
        const extension = file.type

//        console.log(`${name} is ${size} kB, .${extension}.`);

        if (size > 5*1024) {
            button.style.visibility = "hidden";
            textField.innerHTML = "File too big, please select a file less than 5MB.";
            TurnRed();
            HidePreview();
        } else if (allowed_images.indexOf(extension) < 0) {
            button.style.visibility = "hidden";
            textField.innerHTML = "Accepting only jpg, jpeg, png files.";
            TurnRed();
            HidePreview();
        } else {
            button.style.visibility = "visible";
            textField.innerHTML = "File ok.";
            TurnGreen();
            ShowPreview();
        }
    }
}

function TurnRed(){
    var textField = document.getElementById("validationTextField");
    textField.style.color = "rgb(255,0,0)";
}
function TurnGreen(){
    var textField = document.getElementById("validationTextField");
    textField.style.color = "rgb(0,195,0)";
}
function ShowPreview(){
    var file = document.getElementById('upImage').files[0];
    var reader  = new FileReader();
        reader.onload = function(e)  {
            var imgField = document.getElementById("preview");
            imgField.src = e.target.result;
            imgField.style.display = "initial";
            imgField.style['max-height'] = "400px";
            imgField.style['max-width'] = "400px";
            imgField.alt = file.name;
            imgField.title = file.name;
         }
         reader.readAsDataURL(file);

}
function HidePreview(){
    var imgField = document.getElementById("preview");
        imgField.style.display = "none";
}


function PictureClicked(e){
    console.log(e)
}