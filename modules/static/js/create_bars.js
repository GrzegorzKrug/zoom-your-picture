const ids = ["powerBar", "sizeBar"];
const textids = ["powerText", "sizeText"];
const text = ["Power", "Output size"];
const minvals = [50, 50];
const maxvals = [150, 400];
const vals = [100, 300];
const steps = [1, 5];

function CreateBars()  {
    var root = document.getElementById("barContainer");
    root.style.display = "flex";
    root.style["justify-content"] = "center";


    for(i=0; i<ids.length; i++){
        ct = document.createElement("div");
        ct.style.padding = "3px";
        ct.style.margin = "10px";
//        ct.style.width = "10%";

        rng = document.createElement("input");
        rng.type = "range";
        rng.onchange = (name) => {onBarChanged(name)};
        rng.min = minvals[i];
        rng.max = maxvals[i];
        rng.step = steps[i];
        rng.value = vals[i];
        rng.id = ids[i];
        rng.name = ids[i];
        rng.setAttribute("barid", i);

//        rng.style.position = "fixed";
//        rng.style.align = "right";
//        rng.style.left = "35%";
//        rng.style.float = "right";

        tx = document.createElement("span");
        tx.id = "textid" + i;
        tx.innerHTML = text[i] +" " + vals[i]+" px";
        tx.style.position = "relative";
        tx.style.top = '-0.2em';

//        tx.style.position = "fixed";
//        tx.style.left = "50%";
//        tx.style.align = "left";

        ct.appendChild(rng);
        ct.appendChild(tx);
//        ct.style.align = "left";
        root.appendChild(ct);
    }


}

const radioText = [
        "Messenger", "Dex",
        "Google", "Facebook",
        "Joypixels", "Samsung", "Twitter",
        ]

const pics = [
  'messenger_emotes.png', "emojidex_emotes.png",
  "google_emotes.png", "facebook_emotes.png",
  "joypixels_emotes.png", "samsung_emotes.png", "twitter_emotes.png"
]

function CreateRadios()  {
    var root = document.getElementById("radioContainer");
//        root.style.display = "flex";

    for(i=0; i<radioText.length; i++){
        box = document.createElement("container")
        box.setAttribute("class", "palette_preview")

        rad = document.createElement("input");
        rad.type = "radio";
        rad.id = "radio-emoji-" + i;
        rad.name = "palette";
        rad.value = radioText[i].toLowerCase();
        rad.style["margin-left"] = "15px";
        if (i == 0){
            rad.checked = true;
        }
        lab = document.createElement("label");
        tx = document.createElement("i");
        tx.innerHTML = radioText[i];
        tx.style['font-style'] = "normal";
        lab.appendChild(rad);
        lab.appendChild(tx);

        img = document.createElement("img");
        img.src = "/static/emotes/" + pics[i];
        img.setAttribute("class", "preview_image");
        img.style.display = 'inline-block';

//        box.appendChild(lab);
//        box.appendChild(img);

//        root.appendChild(box);
        root.appendChild(lab);
        root.appendChild(img);
    }
}


window.onload = () => {
    CreateBars();
    CreateRadios();
};


function onBarChanged(event){
const i = event.target.attributes.barid.value
const val = event.target.value

search = "textid" + i;
tx = document.getElementById(search);
new_text = text[i] + " " + val + " px";
tx.innerHTML = new_text;

}