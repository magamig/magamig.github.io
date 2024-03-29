---
title: "Real-Time Video Convolution Using WebGL"
date: 2021-05-03T21:00:00+01:00
location: "France"
---

A **convolution** is a mathematical operation that is done by multiplying a pixel’s and its neighboring pixels
color value by a weighted matrix, and then adding those values together (for all the pixels of an image). The small matrix that defines the weights of the multiplication is called **kernel** or convolution matrix. This is used to apply effects to an image such as blurring, sharpening, outlining, and more; where each effect uses a distinct kernel.

The aforementioned technique is also used in the field of deep learning with **convolutional neural networks (CNNs)**. In this context, we try to learn the weights for each element of the convolution matrix in order to improve the score of our model. However, this post is more focused on just understanding how convolutions work.

A convolution can be defined by the following formula: [^2]

[^2]: Song Ho Ahn (안성호). [Convolution](http://www.songho.ca/dsp/convolution/convolution.html#convolution_2d). Digital Signal Processing.

$$ g(x, y)=\omega * f(x, y)=\sum_{d x=-a}^{a} \sum_{d y=-b}^{b} \omega(d x, d y) f(x+d x, y+d y) $$

where $g(x,y)$ is the output filtered image, $f(x, y)$ is the input image and $\omega$ is the kernel. This is pictured in the following animation: [^1]

[^1]: Michael Plotke. [2D Convolution Animation](https://commons.wikimedia.org/wiki/File:2D_Convolution_Animation.gif). Wikimedia Commons.

<video autoplay loop muted playsinline class="center">
    <source src="/video/2d_convolution_animation.mp4" type="video/mp4">
    Your browser doesn't support this embedded video.
</video>

For something more interactive, I highly recommend you to visit "[Image Kernels](https://setosa.io/ev/image-kernels/)" by Victor Powell. There are several examples that already display the process of performing convolutions, so I'm bringing a different approach where we **apply the kernels in real-time to a video feed using WebGL**.

---

In this approach we will be using WebGL - a rasterization engine that draws points, lines, and triangles based on code we supply. To compute what an image will look like and where it is placed, we need to write a program formed by two different functions. These functions are called [shaders](https://en.wikipedia.org/wiki/Shader):

- **Vertex Shader**, responsible for the positions
- **Fragment Shader**, responsible for the colors

But for more material on this topic, visit "[WebGL2 Fundamentals](https://webgl2fundamentals.org/)". Since we want to compute the pixel's new color, we need to implement our logic within the fragment shader. Therefore, all that we do is *"translate"* the previous math formula into code as such:

<pre id="fragment_shader">
precision mediump float;
uniform sampler2D image;
uniform vec2 resolution;
uniform mat3 kernel;
varying vec2 uv;

void main(){
    vec2 cellSize = 1.0 / resolution;
    for(int i=-1; i<=1; i++){
        for(int j=-1; j<=1; j++){
            vec2 vec = cellSize * vec2(float(i), float(j));
            gl_FragColor += 
                texture2D(image, uv + vec) *
                kernel[i][j];
        }
    }
    gl_FragColor[3] = 1.0; //alpha correction
}
</pre>

In this example, we have the particularity of the `vec2 uv` variable which represents the current pixel cooordinates, and the `vec2 cellSize` which is the size of each pixel both horizontally and vertically.  

Afterwards, we just need to perform this computation for each frame from the video feed - and there you have it: **a real-time convolution over a video using WebGL**. For more details on how this is working under the hood, you can check the page source code.

## Visualization

<video src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" crossOrigin="anonymous" controls width=100% id="video" muted autoplay>
	Your browser does not support the video tag.
</video><br/>
<canvas id="canvas" width="500" height="300"></canvas><br/>

<div class="row">
    <b>Test a different kernel:</b><br/>
    <form name="kernelform" class="col">
        <input type="radio" name="kernel" value="[0,0,0,0,1,0,0,0,0]"> Identity</input><br/>
        <input type="radio" name="kernel" value="[1,1,1,1,-8,-1,1,1,1]" checked> Laplacian Edge Detection</input><br/>
        <input type="radio" name="kernel" value="[0.0625,0.125,0.0625,0.125,0.250,0.125,0.0625,0.125,0.0625]"> Gaussian Blur</input><br/>
        <input type="radio" name="kernel" value="[0.111,0.111,0.111,0.111,0.111,0.111,0.111,0.111,0.111]"> Box Blur</input><br/>
        <input type="radio" name="kernel" value="[0,-1,0,-1,5,-1,0,-1,0]"> Sharpen</input><br/>
        <input type="radio" name="kernel" value="[-1,-1,-1,-1,9,-1,-1,-1,-1]"> Unsharpen</input><br/>
    </form>
    <table id="kernelviz" class="matrix col">
        <tr>
            <td>1</td>
            <td>1</td>
            <td>1</td>
        </tr>
        <tr>
            <td>1</td>
            <td>-8</td>
            <td>1</td>
        </tr>
        <tr>
            <td>1</td>
            <td>1</td>
            <td>1</td>
        </tr>
    </table>
</div>

<script>
	const canvas = document.getElementById("canvas");
    const video = document.getElementById("video");
    const kernelform = document.forms.kernelform;
    const kernelviz = document.getElementById("kernelviz");

    // matrix update on radio change
    const chunk = (array, size) => Array.from({length: Math.ceil(array.length / size)}, (value, index) => array.slice(index * size, index * size + size));
    document.addEventListener("input", function(e) {
        if(e.target.getAttribute("name") == "kernel") {
            let value = eval(e.target.value);
            value = value.map(e => "<td>" + e + "</td>");
            value = chunk(value,3);
            value = value.map(e => "<tr>" + e.join("") + "</tr>").join("");
            kernelviz.innerHTML = value;
        }
    });

    video.oncanplay = function() {
        canvasResize();
        loadShaders();
    };

    function canvasResize() {
        let videoComputedStyle = getComputedStyle(video);
        canvas.width = parseFloat(videoComputedStyle.width); 
        canvas.height = parseFloat(videoComputedStyle.height);
    }
    
    function loadShaders() {
        let gl = null;
        let gl_contextAttributes = { antialias:false };
        for (let i=0; i<4; i++) {
            gl = canvas.getContext(["webgl","experimental-webgl","moz-webgl","webkit-3d"][i], gl_contextAttributes)
            if (gl)
                break;
        }
        
        let vs = gl.createShader(gl.VERTEX_SHADER);
        gl.shaderSource(vs, `
            attribute vec2 vx;
            varying vec2 uv;
            
            void main(){
                gl_Position = vec4(vx.x*2.0-1.0, 1.0-vx.y*2.0, 0, 1);
                uv = vx;
            }
        `);
        gl.compileShader(vs);

        let ps = gl.createShader(gl.FRAGMENT_SHADER);
        gl.shaderSource(ps, document.getElementById("fragment_shader").innerText);
        gl.compileShader(ps);

        let shader  = gl.createProgram();
        gl.attachShader(shader, vs);
        gl.attachShader(shader, ps);
        gl.linkProgram(shader);
        gl.useProgram(shader);

        // basic attributes
        let vx_ptr = gl.getAttribLocation(shader, "vx");
        gl.enableVertexAttribArray(vx_ptr);
        let vx = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vx);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0,0, 1,0, 1,1, 0,1]), gl.STATIC_DRAW);
        let ix = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ix);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array([0,1,2, 0,2,3]), gl.STATIC_DRAW);
        let tex = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D, tex);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T,     gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S,     gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        
        // custom attributes
        let resolution = gl.getUniformLocation(shader,"resolution");
        gl.uniform2fv(resolution, [canvas.width, canvas.height]);  
        let kernel = gl.getUniformLocation(shader,"kernel");

        function frameloop() {
            // pass kernel
            let selectedKernel = kernelform.querySelector("input[name=kernel]:checked").value;
            gl.uniformMatrix3fv(kernel, false, eval(selectedKernel));

            // basic gl video play
            gl.clear(gl.COLOR_BUFFER_BIT);
            gl.activeTexture(gl.TEXTURE0);
            gl.bindTexture(gl.TEXTURE_2D, tex);
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, video);
            gl.bindBuffer(gl.ARRAY_BUFFER, vx);
            gl.vertexAttribPointer(vx_ptr, 2, gl.FLOAT, false, 0, 0);
            gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ix);
            gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, 0);
            window.requestAnimationFrame(frameloop);
        }
        frameloop();
    }
</script>

<style>
.row {
    margin: 20px 0;
}
.col {
    vertical-align: middle;
    display:inline-block;
    margin: 10px;
}
.matrix {
    display:inline-block;
    position: relative;
    margin: 30px;
}
.matrix:before, .matrix:after {
    content: "";
    position: absolute;
    top: 0;
    border: 1px solid #000;
    width: 6px;
    height: 100%;
}
.matrix:before {
    left: -6px;
    border-right: 0px;
}
.matrix:after {
    right: -6px;
    border-left: 0px;
}
.matrix td {
    padding: 5px 15px;    
    text-align: center;
}
video::-webkit-media-controls-fullscreen-button {
    display: none;
}
</style>