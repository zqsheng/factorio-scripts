import * as thr from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';


const scene = new thr.Scene();
const camera = new thr.PerspectiveCamera( 75, 1, 0.1, 1000 );

console.log("width: ", window.innerWidth, "height: ", window.innerHeight);

const renderer = new thr.WebGLRenderer();
renderer.setSize(1000, 1000);
renderer.setAnimationLoop(animate);
document.body.appendChild(renderer.domElement);

const geometry = new thr.BoxGeometry( 1, 1, 1 );
const material = new thr.MeshBasicMaterial( { color: 0x00ff00 } );
const cube = new thr.Mesh( geometry, material );

camera.position.z = 100;
camera.position.x = 0 ;
camera.position.y = 0 ;
camera.lookAt(0, 0, 0);  
console.log(camera);

const dice_width = 8;

const controls = new OrbitControls( camera, renderer.domElement );


controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
controls.dampingFactor = 0.05;

controls.screenSpacePanning = false;

controls.minDistance = 100;
controls.maxDistance = 500;

controls.maxPolarAngle = Math.PI/2;


// material
// - MeshBasicMaterial, is not affected by lights.
// - MeshLambertMaterial, computes lighting only at the vertices.
// - MeshPhongMaterial which computes lighting at every pixel.  The MeshPhongMaterial also supports specular highlights.

const loader = new thr.TextureLoader();
const materials = [
	  new thr.MeshBasicMaterial({map: loadColorTexture('resources/dice_1.png')}),
	  new thr.MeshBasicMaterial({map: loadColorTexture('resources/dice_2.png')}),
	  new thr.MeshBasicMaterial({map: loadColorTexture('resources/dice_3.png')}),
	  new thr.MeshBasicMaterial({map: loadColorTexture('resources/dice_4.png')}),
	  new thr.MeshBasicMaterial({map: loadColorTexture('resources/dice_5.png')}),
	  new thr.MeshBasicMaterial({map: loadColorTexture('resources/dice_6.png')})
];

const xAxisMaterial = new thr.MeshBasicMaterial({color: 0xff0000});
const xAxisGeometry = new thr.BufferGeometry().setFromPoints([new thr.Vector3(0, 0, 0), new thr.Vector3(40, 0, 0)]);
const xAxisMesh= new thr.Line(xAxisGeometry, xAxisMaterial);
scene.add(xAxisMesh)
	
const yAxisMaterial = new thr.MeshBasicMaterial({color: 0x00ff00});
const yAxisGeometry = new thr.BufferGeometry().setFromPoints([new thr.Vector3(0, 0, 0), new thr.Vector3(0, 40, 0)]);
const yAxisMesh= new thr.Line(yAxisGeometry, yAxisMaterial);
scene.add(yAxisMesh)
 
const zAxisMaterial = new thr.MeshBasicMaterial({color: 0x0000ff});
const zAxisGeometry = new thr.BufferGeometry().setFromPoints([new thr.Vector3(0, 0, 0), new thr.Vector3(0, 0, 40)]);
const zAxisMesh= new thr.Line(zAxisGeometry, zAxisMaterial);
scene.add(zAxisMesh)

function loadColorTexture( path ) {
	  const texture = loader.load( path );
	  texture.colorSpace = thr.SRGBColorSpace;
	  return texture;
}

const color = 0xFFFFFF;
const intensity = 3;
const light = new thr.DirectionalLight( 'lightblue', intensity );
light.position.set( - 1, 2, 4 );
scene.add( light );

let dice_geometry  = new thr.BoxGeometry(dice_width, dice_width, dice_width, 1, 1, 1);
let dice_material = new thr.MeshPhongMaterial( { color: '0xaa8844' } );
let dice = new thr.Mesh(dice_geometry, materials);
scene.add(dice);

dice.name = 'dice';
const times = [0, 1, 2, 3];

const xAxis = new thr.Vector3(1,0,0);

const rotateValues = [];
for(let i = 0; i < times.length; i++) {
	const q = new thr.Quaternion().setFromAxisAngle(xAxis, Math.PI/2*i)
	rotateValues.push(q.x,q.y,q.z,q.w);
}

const rotateKF = new thr.QuaternionKeyframeTrack('dice.quaternion', times, rotateValues);
const clip = new thr.AnimationClip("dice_clip", 3, [rotateKF]);

const mixer = new thr.AnimationMixer(dice);
const action = mixer.clipAction(clip);
action.play();

const clock = new thr.Clock();

let lastTime = -1;

console.log("init quaternion: ", dice);

const boxEulers = [];
boxEulers.push(new thr.Euler(0, 0, 0, 'XYZ'));
boxEulers.push(new thr.Euler(Math.PI/2, 0, 0, 'XYZ'));
boxEulers.push(new thr.Euler(Math.PI, 0, 0, 'XYZ'));
boxEulers.push(new thr.Euler(Math.PI/2*3, 0, 0, 'XYZ'));
boxEulers.push(new thr.Euler(0, Math.PI/2, 0, 'XYZ'));


function animate() {
	let t = Math.ceil(clock.getElapsedTime());
	controls.update();
	
	if ((Math.ceil(t) & 1) == 0 && t > lastTime) {
		lastTime  = t;
		let val = Math.floor(Math.random()*boxEulers.length);
		let e = boxEulers[val];
		dice.rotation.x = e.x;
		dice.rotation.y = e.y;
		dice.rotation.z = e.z;
	}
	renderer.render(scene, camera);
}
{
	const audioContext = new (window.AudioContext || window.webkitAudioContext)();
	const reader = new FileReader();
	const barWidth = 2;
	const gap = 1;
	
}
import rough from 'roughjs';
{
	let rc = rough.canvas(document.getElementById('2d_geometry'));
	let x = 50, y = 50, diameter = 25, width = 100;
	
	// 1
	rc.rectangle(x,y, width, width);
	rc.circle(x+width/2,y+width/2, diameter, {fill: 'red' });
	// 2
	x += 110;
	rc.rectangle(x,y, width, width);
	rc.circle(x+width/2 +15,y+width/2 +15, diameter, {fill: 'blue' });
	rc.circle(x+width/2 -15,y+width/2 -15, diameter, {fill: 'blue' });
	//3
	x += 110;
	rc.rectangle(x,y, width, width);
	rc.circle(x+width/2,y+width/2, diameter, {fill: 'red' });
	rc.circle(x+width/2+diameter,y+width/2+diameter, diameter, {fill: 'red' });
	rc.circle(x+width/2-diameter,y+width/2-diameter, diameter, {fill: 'red' });
	// 4
	x += 110;
	rc.rectangle(x,y, width, width);
	rc.circle(x+width/2+diameter,y+width/2+diameter, diameter, {fill: 'blue' });
	rc.circle(x+width/2-diameter,y+width/2-diameter, diameter, {fill: 'blue' });
	rc.circle(x+width/2+diameter,y+width/2-diameter, diameter, {fill: 'blue' });
	rc.circle(x+width/2-diameter,y+width/2+diameter, diameter, {fill: 'blue' });
	// 5
	x += 110;
	rc.rectangle(x,y, width, width);
	rc.circle(x+width/2,y+width/2, diameter, {fill: 'red' });
	rc.circle(x+width/2+diameter,y+width/2+diameter, diameter, {fill: 'red' });
	rc.circle(x+width/2-diameter,y+width/2-diameter, diameter, {fill: 'red' });
	rc.circle(x+width/2+diameter,y+width/2-diameter, diameter, {fill: 'red' });
	rc.circle(x+width/2-diameter,y+width/2+diameter, diameter, {fill: 'red' });
	// 6
	x += 110;
	rc.rectangle(x,y, width, width);
	rc.circle(x+width/2+diameter,y+width/2+diameter, diameter, {fill: 'blue' });
	rc.circle(x+width/2-diameter,y+width/2-diameter, diameter, {fill: 'blue' });
	rc.circle(x+width/2+diameter,y+width/2-diameter, diameter, {fill: 'blue' });
	rc.circle(x+width/2-diameter,y+width/2+diameter, diameter, {fill: 'blue' });
	rc.circle(x+width/2-diameter,y+width/2, diameter, {fill: 'blue' });
	rc.circle(x+width/2+diameter,y+width/2, diameter, {fill: 'blue' });
}
