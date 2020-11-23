(function(){
    var clockrad = 110;
    var clockx = clockrad+15;
    var clocky =  clockrad+15;

    var c = document.getElementById("canvas10h");
    var ctx = c.getContext("2d");

    function get_10_time(){
      var d = new Date();
      var n = d.getTime();
      whole_day = 60*60*24;
      cur_time = (n/1000) % whole_day;

      hour = cur_time / whole_day;
      min = parseInt(hour *10 * 100)%100/100;
      sec = parseInt(hour *10 * 10000)%100/100;

    //   ctx.fillStyle = "rgb(0,0,0)";
    //   ctx.font = "30px Verdaba";
    //   ctx.fillText(parseInt(hour*10)+":"+min+":"+sec, 100, 300)
    //   ctx.fillText(hour, 100, 350)
      return [hour, min, sec];
    }

    function draw_10clock(){
      ctx.fillStyle = "rgb(70,70,90)";
      ctx.clearRect(0, 0, c.width, c.height);

      draw_clock_skelet()
      draw_10clock_labels()

      out = get_10_time();
      hour = out[0];
      min = out[1];
      sec = out[2];

      //     draw_arrow(0, 30);
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

    function draw_10clock_labels(){
      ctx.save();
      ctx.font='bold 20px Verdana';
      ctx.textAlign = "center";
      ctx.fillStyle = "rgb(25,50,90)";
      for(i=1;i<=100;i++){
        posx = clockx + Math.sin(-i/50*Math.PI+Math.PI)*(clockrad-30)
        posy = clocky + Math.cos(i/50*Math.PI+Math.PI)*(clockrad-30)+7
        if ((i/10)%1 == 0){
          ctx.fillText(i/10, posx, posy);
          ctx.lineWidth=4;
          lindist = 13
        }
        else{
          ctx.lineWidth=2;
          lindist = 6
        }
        ctx.beginPath();
        bd = 7

        startx = clockx + Math.sin(-i/50*Math.PI+Math.PI)*(clockrad-bd)
        starty = clocky + Math.cos(i/50*Math.PI+Math.PI)*(clockrad-bd)
        endx = clockx + Math.sin(-i/50*Math.PI+Math.PI)*(clockrad-bd-lindist)
        endy = clocky + Math.cos(i/50*Math.PI+Math.PI)*(clockrad-bd-lindist)

        ctx.moveTo(startx, starty);

        ctx.lineTo(endx, endy);
        ctx.stroke();
      }
      ctx.restore();
    }


    function animate10() {
        window.requestAnimationFrame(animate10);
        draw_10clock();
    }

    animate10();
})();