const ids = ["powerBar", "sizeBar"];
const textids = ["powerText", "sizeText"];
const text = ["Power", "Output size"];

const zoom_minvals = [50, 50];
const zoom_maxvals = [150, 400];
const mozaic_minvals = [50, 50];
const mozaic_maxvals = [150, 1000];

const zoom_vals = [100, 300];
const mozaic_vals = [100, 500];

const steps = [1, 5];

function CreateBars()  {
    var root = document.getElementById("barContainer");
    root.style.display = "flex";
    root.style["justify-content"] = "center";


    for(i=0; i<ids.length; i++){
        ct = document.createElement("div");
        ct.style.padding = "3px";
        ct.style.margin = "10px";

        rng = document.createElement("input");
        rng.type = "range";
        rng.onchange = (name) => {onBarChanged(name)};
        rng.min = mozaic_minvals[i];
        rng.max = mozaic_maxvals[i];
        rng.step = steps[i];
        rng.value = mozaic_vals[i];
        rng.id = ids[i];
        rng.name = ids[i];
        rng.setAttribute("barid", i);

        tx = document.createElement("span");
        tx.id = "textid" + i;
        tx.innerHTML = text[i] +" " + mozaic_vals[i]+" px";
        tx.style.position = "relative";
        tx.style.top = '-0.2em';

        ct.appendChild(rng);
        ct.appendChild(tx);

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

const modes = [
  "Mozaic",
  "Zoom"
]

function CreatePaletteRadios()  {
    var root = document.getElementById("radioContainer");
    for(i=0; i<radioText.length; i++){
        rad = document.createElement("input");
        rad.type = "radio";
        rad.id = "radio-emoji-" + i;
        rad.name = "palette";
        rad.value = radioText[i].toLowerCase();
        rad.style["margin-left"] = "15px";
        if (i == 5){
            rad.checked = true;
        }
        lab = document.createElement("label");
        lab.setAttribute("class", "palette_radio")


        tx = document.createElement("i");
        tx.innerHTML = radioText[i];
        tx.style['font-style'] = "normal";
        if (i == 0 || i == 5){
          tx.style['font-weight'] = 100;
          tx.style['text-shadow'] = "0 0 10px rgb(00,245,0)";
        }
        if (i == 2 || i == 3){
          tx.style['text-shadow'] = "0 0 20px rgb(00,185,0)";
        }

        lab.appendChild(rad);
        lab.appendChild(tx);
        lab.style['text-align'] = "left";
//        lab.style['border-top'] = "1px solid rgb(0,0,0)";

        img = document.createElement("img");
        img.src = "/static/emotes/" + pics[i];
        img.setAttribute("class", "preview_palette");
        img.style.display = 'block';

        root.appendChild(lab);
        root.appendChild(img);
    }
}

function CreateModeRadios() {
    var root = document.getElementById("modeContainer");

    for(i=0; i<modes.length; i++){
      radio = document.createElement("input");
      txt = document.createElement("i");
      label = document.createElement("label");

      radio.type = 'radio';
      radio.name = "mode";
      radio.value = i;
      radio.id = "mode" + i;
      if (i == 0){
        radio.checked = true;
      }

      radio.onclick = (name) => checkSelectedMode();
      txt.innerHTML = modes[i];
      label.appendChild(radio);
      label.append(txt);
      label.setAttribute("class", "gridElement");
      root.appendChild(label);

      // Create element in next column
      label = document.createElement("label")
      label.setAttribute("class", "gridElement");

      if (i == 0){

        check = document.createElement("input");
        check.type = "checkbox";
        check.name = "makeBigger";
        check.value = true;

        txt = document.createElement("i");
        txt.innerHTML = "Double size, but JPG";
        txt.style['font-style'] = 'normal';
        txt.style['font-size'] = '0.8em';
        label.appendChild(txt);
        label.appendChild(check);

        root.appendChild(label)
      }
      else{
        // Add empty label
        root.appendChild(label)
      }
    }

}

window.onload = () => {
    CreateBars();
    CreatePaletteRadios();
    CreateModeRadios();
};

function checkSelectedMode(){
  console.log("Checking");
  for (i=0; i<ids.length; i++){
    slider = document.getElementById("mode" + i);
    if (slider.checked == true){
      if (i == 0){
        setMozaicParams();
      }
      if (i == 1){
        setZoomParams();
      }
    }
  }
}


function setMozaicParams(){
 for (i=0; i<ids.length; i++){
   slider = document.getElementById(ids[i]);
   slider.min = mozaic_minvals[i];
   slider.max = mozaic_maxvals[i];
   slider.value = mozaic_vals[i];
   tx = document.getElementById("textid" + i);
   tx.innerHTML = text[i] +" " + mozaic_vals[i]+" px";
 }
}

function setZoomParams(){
 for (i=0; i<ids.length; i++){
   slider = document.getElementById(ids[i]);
   slider.min = zoom_minvals[i];
   slider.max = zoom_maxvals[i];
   slider.value = zoom_vals[i];

   tx = document.getElementById("textid" + i);
   tx.innerHTML = text[i] +" " + zoom_vals[i]+" px";
 }
}



function onBarChanged(event){
const i = event.target.attributes.barid.value
const val = event.target.value

search = "textid" + i;
tx = document.getElementById(search);
new_text = text[i] + " " + val + " px";
tx.innerHTML = new_text;

}