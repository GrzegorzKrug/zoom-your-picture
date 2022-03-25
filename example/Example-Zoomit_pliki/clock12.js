var clockrad = 110;
var clockx = clockrad+15;
var clocky =  clockrad+15;
var timezoneOffset = 0;

var plateColor = "rgb(235, 235, 255)";
var borderColor = "rgb(150, 160, 195)";
var plateLineColor = "rgb(0,50,50)";
var innerPlateLineColor = "rgb(40,0,0)";
var plateLineThickness = 3;
var borderSize = 15;

var bigLineColor = "rgb(200,0,0)";
var smallLineColor = "rgb(130,130,130)";

var labelColor = "rgb(25,50,90)";
var arrowStickColor = "rgb(10, 120, 1155)";
var arrowStickWidth = 5;
var arrowHeadLineWidth = 3;

var fastArrowColor = "rgb(50,50,510)";
var mediumArrowColor = "rgb(240,80,180)";
var slowArrowColor = "rgb(255,150,0)";

var fastArrowLenght = 70;
var mediumArrowLenght = 60;
var slowArrowLenght = 40;

(function(){
    var clockrad = 110;
    var clockx = clockrad+15;
    var clocky =  clockrad+15;

    var c = document.getElementById("canvas12h");
    var ctx = c.getContext("2d");

    function get_12_time(){
      var d = new Date();
      var n = d.getTime() + timezoneOffset;
      whole_day = 60*60*24;
      cur_time = (n/1000) % whole_day;

      hour = (cur_time) / (whole_day)*2;
      min = parseInt(cur_time/60) %60/60;
      sec = parseInt(cur_time) %60/60;

      return [hour, min, sec];
    }

    function draw_12_clock(){
//      ctx.fillStyle = "rgb(70,70,90)";
      ctx.clearRect(0, 0, c.width, c.height);

      draw_clock_skelet();
      draw_12_clock_labels();

      out = get_12_time();
      hour = out[0];
      min = out[1];
      sec = out[2];

      draw_arrow(sec*Math.PI*2, fastArrowLenght, fastArrowColor);
      draw_arrow(min*Math.PI*2, mediumArrowLenght, mediumArrowColor);
      draw_arrow(hour*Math.PI*2, slowArrowLenght, slowArrowColor);
    }

    function draw_clock_skelet(){
      ctx.save();
      ctx.fillStyle = plateColor;
      ctx.strokeStyle = borderColor;
      ctx.lineWidth = borderSize;

      ctx.beginPath();
      ctx.arc(clockx, clocky, clockrad, 0, 2 * Math.PI);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      ctx.beginPath();
      ctx.strokeStyle = innerPlateLineColor;
      ctx.lineWidth = plateLineThickness;
      ctx.arc(clockx, clocky, clockrad-borderSize/2, 0, 2 * Math.PI);
      ctx.stroke();

      ctx.beginPath();
      ctx.strokeStyle = plateLineColor;
      ctx.arc(clockx, clocky, clockrad+borderSize/2, 0, 2 * Math.PI);
      ctx.stroke();

      ctx.beginPath();
      ctx.strokeStyle = arrowStickColor;
      ctx.fillStyle = arrowStickColor;
      ctx.arc(clockx, clocky, 3, 0, 2*Math.PI);
      ctx.closePath();
      ctx.fill();
      ctx.stroke()

      ctx.restore();
    }

    function draw_arrow(rot, size, color){
        ctx.save();
        ctx.strokeStyle = arrowStickColor;
        ctx.lineWidth = arrowStickWidth;
        ctx.lineWidth = arrowStickWidth;

        ctx.beginPath();
        ctx.moveTo(clockx, clocky);
        desx = clockx + Math.sin(rot)*size;
        desy = clocky - Math.cos(rot)*size;

        ctx.lineTo(desx, desy);
        ctx.stroke();
        draw_arrow_head(desx, desy, rot, 40, color);

        ctx.restore();
    }

    function draw_arrow_head(x, y, rot, size, color){
      ctx.save()
      headx = Math.sin(rot)*size/3;
      heady = Math.cos(rot)*size/3;
      head_sidex = Math.sin(rot+Math.PI/2)*(size/15+2);
      head_sidey = Math.cos(-rot+Math.PI/2)*(size/15+2);

      ctx.beginPath();
      ctx.strokeStyle = arrowStickColor;
      ctx.lineWidth = arrowHeadLineWidth;
      ctx.fillStyle = color;

      ctx.moveTo(x+headx, y-heady);
      ctx.lineTo(x+head_sidex, y+head_sidey);
      ctx.lineTo(x-head_sidex, y-head_sidey);
      ctx.closePath();

      ctx.stroke();
      ctx.fill()
      ctx.restore();
    }

    function draw_12_clock_labels(){
      ctx.save();
      ctx.font='bold 20px Verdana';
      ctx.textAlign = "center";
      ctx.fillStyle = labelColor;
      fullrange = 60;
      plates = 12;
      spacing = fullrange/plates;
      bd = borderSize/2+plateLineThickness/2

      for(i=1;i<=fullrange;i++){
        posx = clockx + Math.sin(-i/fullrange*2*Math.PI+Math.PI)*(clockrad-bd-13-12)
        posy = clocky + Math.cos(i/fullrange*2*Math.PI+Math.PI)*(clockrad-bd-13-12)+8
        if ((i%spacing) == 0){
          ctx.fillText(i/spacing, posx, posy);
          lindist = 13
          ctx.lineWidth = 5;
          ctx.strokeStyle = bigLineColor;
        }
        else{
          ctx.lineWidth = 4;
          lindist = 7;
          ctx.strokeStyle = smallLineColor;
        }
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


    function animate12() {
        window.requestAnimationFrame(animate12);
        draw_12_clock();
    }

    animate12();
})();