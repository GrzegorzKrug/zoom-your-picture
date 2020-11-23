var clockrad = 110;
var clockx = clockrad+15;
var clocky =  clockrad+15;

var c = document.getElementById("canvas8h");
var ctx = c.getContext("2d");

function get_8_time(){
  var d = new Date();
  var n = d.getTime();
  whole_day = 60*60*24;
  cur_time = (n/1000) % whole_day;

  hour = cur_time / whole_day;
  min = parseInt(cur_time/100) %100/100;
  sec = parseInt(cur_time) %100/100;

  return [hour, min, sec];
}

function draw_8clock(){
  ctx.fillStyle = "rgb(70,70,90)";
  ctx.clearRect(0, 0, c.width, c.height);

  draw_clock_skelet()
  draw_24clock_labels()

  out = get_8_time();
  hour = out[0];
  min = out[1];
  sec = out[2];

  draw_arrow(hour*Math.PI*2, 80);
  draw_arrow(min*Math.PI*2, 60);
  draw_arrow(sec*Math.PI*2, 40);
}

function draw_clock_skelet(){
  ctx.save();
  ctx.fillStyle = "rgb(235, 235, 255)";
  ctx.strokeStyle = "rgb(150, 160, 195)";
  border = 15
  ctx.lineWidth = border;


  ctx.beginPath();
//   ctx.ellipse(clockx, clocky, clockrad, clockrad, 0, 3)
  ctx.arc(clockx, clocky, clockrad, 0, 2 * Math.PI);
  ctx.closePath();

  ctx.fill();
  ctx.stroke();

  ctx.strokeStyle = "rgb(0,0,0)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(clockx, clocky, clockrad-border/2, 0, 2 * Math.PI);
//   ctx.closePath();

  ctx.stroke();
  ctx.beginPath();
  ctx.arc(clockx, clocky, clockrad+border/2, 0, 2 * Math.PI);
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(clockx, clocky, 3, 0, 2*Math.PI);
  ctx.closePath();
  ctx.fillStyle = "rgb(0, 0, 0)";
  ctx.fill();
  ctx.stroke()

  ctx.restore();

}

function draw_arrow(rot, size){
    ctx.save();
    ctx.strokeStyle = "rgb(0,0,0)";
    ctx.beginPath();
    ctx.moveTo(clockx, clocky);
    desx = clockx + Math.sin(rot)*size;
    desy = clocky - Math.cos(rot)*size;

    ctx.lineTo(desx, desy);
    ctx.lineWidth = 5;
    ctx.stroke();
    draw_arrow_head(desx, desy, rot, 40);

    ctx.restore();
}

function draw_arrow_head(x, y, rot, size){
  ctx.save()
  headx = Math.sin(rot)*size/3;
  heady = Math.cos(rot)*size/3;
  head_sidex = Math.sin(rot+Math.PI/2)*(size/15+2);
  head_sidey = Math.cos(-rot+Math.PI/2)*(size/15+2);

  ctx.beginPath();
  ctx.moveTo(x+headx, y-heady);
  ctx.lineTo(x+head_sidex, y+head_sidey);
  ctx.lineTo(x-head_sidex, y-head_sidey);
  ctx.closePath();

  ctx.strokeStyle = "rgb(0,0,0)";
  ctx.lineWidth = 3;
  ctx.fillStyle = "rgb(0, 100, 255)";
  ctx.stroke();
  ctx.fill()
  ctx.restore();
}

function draw_24clock_labels(){
  ctx.save();
  ctx.font='bold 20px Verdana';
  ctx.textAlign = "center";
  ctx.fillStyle = "rgb(25,50,90)";
  fullrange = 100;
  bd = 7;
  plates = [8.64, 1,2,3,4,5,6,7]

  for(i=0;i<8;i++){
    posx = clockx + Math.sin(-i/8*2*Math.PI+Math.PI)*(clockrad-32)
    posy = clocky + Math.cos(i/8*2*Math.PI+Math.PI)*(clockrad-32)+9
    ctx.fillText(plates[i], posx, posy);
    ctx.lineWidth=4;
    lindist = 13;
    ctx.beginPath();
    startx = clockx + Math.sin(-i/8*2*Math.PI+Math.PI)*(clockrad-bd)
    starty = clocky + Math.cos(i/8*2*Math.PI+Math.PI)*(clockrad-bd)
    endx = clockx + Math.sin(-i/8*2*Math.PI+Math.PI)*(clockrad-bd-lindist)
    endy = clocky + Math.cos(i/8*2*Math.PI+Math.PI)*(clockrad-bd-lindist)
    ctx.moveTo(startx, starty);
    ctx.lineTo(endx, endy);
    ctx.stroke();
  }
  for(i=1;i<=fullrange;i++){

    ctx.lineWidth=2;
    lindist = 6

    ctx.beginPath();


    startx = clockx + Math.sin(-i/fullrange*2*Math.PI+Math.PI)*(clockrad-bd)
    starty = clocky + Math.cos(i/fullrange*2*Math.PI+Math.PI)*(clockrad-bd)
    endx = clockx + Math.sin(-i/fullrange*2*Math.PI+Math.PI)*(clockrad-bd-lindist)
    endy = clocky + Math.cos(i/fullrange*2*Math.PI+Math.PI)*(clockrad-bd-lindist)
    ctx.moveTo(startx, starty);
    ctx.lineTo(endx, endy);
    ctx.stroke();
  }
  ctx.restore();
}


function animate8() {
    window.requestAnimationFrame(animate8);
    draw_8clock();
}

animate8();