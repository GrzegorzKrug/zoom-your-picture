const ids = ["powerBar", "sizeBar"];
const textids = ["powerText", "sizeText"];
const text = ["Power", "Output size"];
const minvals = [50, 50];
const maxvals = [200, 500];
const vals = [150, 500];
const steps = [1, 5];

function CreateBars()  {
    var root = document.getElementById("barContainer");
    root.style.display = "flex";
    root.style["justify-content"] = "center";


    for(i=0; i<ids.length; i++){
        ct = document.createElement("div");
        ct.style.padding = "3px";
        ct.style.background = "rgb(230,250,250)";
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

        console.log(i);
    }


    console.log("CREATED!");

}

const radioText = [
        "Messenger", "Dex",
        "Google", "Facebook",
        "Joypixels", "Samsung", "Twitter",
        ]

function CreateRadios()  {
    var root = document.getElementById("radioContainer");
//        root.style.display = "flex";

    for(i=0; i<radioText.length; i++){
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
        root.appendChild(lab);
    }
}


window.onload = () => {
    CreateBars();
    CreateRadios();
};


function onBarChanged(event){
console.log(event);
const i = event.target.attributes.barid.value
const val = event.target.value
console.log(i);

search = "textid" + i;
console.log(search);
tx = document.getElementById(search);
//console.log(tx);
new_text = text[i] + " " + val + " px";
//console.log(new_text);
tx.innerHTML = new_text;

}