drawCanvas = function() {
    var c = document.getElementById("lineCanvas");
    console.log(c);
    var ctx = c.getContext("2d");
    ctx.beginPath();

    var left = 1030;
    var right = 1110;
    var width = 150;
    var height = 425;

    ctx.moveTo(left, width);
    ctx.lineTo(right, height);
    ctx.stroke();


    for (var i = 0; i < 13; i++) 
    {
        left = left - 80;
        right = right - 80;
        var ptx = c.getContext("2d");
        ptx.beginPath();
        ptx.moveTo(left, width);
        ptx.lineTo(right, height);
        ptx.stroke();
    };
}
$(function() {
    drawCanvas();   
});