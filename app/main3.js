import * as Matter from 'matter-js'
// module aliases
var Engine = Matter.Engine,
	Render = Matter.Render,
	Runner = Matter.Runner,
	Bodies = Matter.Bodies,
	Composite = Matter.Composite;

// create an engine
var engine = Engine.create();
 engine.gravity.y = 0;

// create a renderer
var render = Render.create({
	element: document.body,
	engine: engine
});

// create two boxes and a ground

var box_width = 20;

var boxes = []
for(var j = 20; j < 400; j+= 31) {
	for(var i = 20; i < 600; i += 31) {
		boxes.push(Bodies.rectangle(i, j, box_width, box_width));
	}
}
boxes[01].color
var ground = Bodies.rectangle(400, 610, 810, 60, { isStatic: true });
boxes.push(ground);


// add all of the bodies to the world
Composite.add(engine.world, boxes);

// run the renderer
Render.run(render);

// create runner
var runner = Runner.create();

// run the engine
Runner.run(runner, engine);
