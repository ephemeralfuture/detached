int num_strings = 16; //defines the number of strings that the program will run
int ellipse_transparency =22; //transparency level for ellipses

int pick_mode = 0; //picks whether it's lightning, articles or strings (or all)
int timer = 0; // a timer for the work

//Below are declarations for arrays that store the bezier positions and curve placements 
int[] bezX1 = new int[num_strings];
int[] bezY1 = new int[num_strings];
int[] bezX2 = new int[num_strings];
int[] bezY2 = new int[num_strings];

int[] CPX1 = new int[num_strings];
int[] CPY1 = new int[num_strings];
int[] CPX2 = new int[num_strings];
int[] CPY2 = new int[num_strings];

float[] bez_stroke = new float[num_strings]; //the stroke weight of the bezier curves is determined when the program loads

int changing_circle1 = 0; //size of an expanding/contracting circle
boolean circle_blink = true; //for turning on and off the expansion/contraction of a circle

int the_saved_frame = 0; //a counter for saving frames for generating movies
int video_num = 3;

String[] gibberish; //this is used to load in the gibberish articles

PFont newspaper; //the font for use here

//The following two variables are used for adjusting the specific
//rects and ellipses by small amounts to fit in the physical frame of the sculpture
float adjustmentX = 33;
float adjustmentY = 88;

void setup() {
  //fullScreen();
  size(1920, 1080); //the size of the monitors is 1920x1080 so I am exporting videos to this size
  frameRate(5);
  for (int x = 0; x < num_strings; x++) { //for loop to set up the bezier curves
    bezX1[x] = 0;
    bezY1[x] = x*height/num_strings;
    bezX2[x] = width;
    bezY2[x] = x*height/num_strings;
    bez_stroke[x] = random(0.5, 15);
    CPX1[x] = int(random(width));
    CPY1[x] = int(random(height));
    CPX2[x] = int(random(width));
    CPY2[x] = int(random(height));
  }
  ellipseMode(CORNER);
  rectMode(CORNER);
  gibberish = loadStrings("data/jcc_generated_gibberish.txt"); //loads the gibberish text
  newspaper = loadFont("GENSCO-48.vlw");
  textFont(newspaper, 30);
  textAlign(LEFT, BASELINE);
}

void draw() {
  background(0);
  noFill();
  stroke(255);
  float the_functions = random(1);
  if (timer >= 100){
    if (the_functions < 0.3){
      pick_mode = 0;
    }else if (the_functions >= 0.3 && the_functions < 0.6){
      pick_mode = 1;
    }else if (the_functions > 0.6 && the_functions < 0.9){
      pick_mode = 2;
    }else if (the_functions >= 0.9){
      pick_mode = 3;
    }
    timer = 0;
  }
  if (pick_mode == 0){
    string_figures(); //a function to draw the wobbly string figures
  }else if (pick_mode == 1){
    ellipse_gaps(); //a function to place the ellipses and rectangles
  }else if (pick_mode == 2){
    articles(); //a function to create the random news articles
  }else if (pick_mode == 3){
    string_figures();
    ellipse_gaps();
    articles();
  }
  timer++;
  if (the_saved_frame < 900){ //this is for saving frames to export films
    saveFrame("stillframes/video"+video_num+"/string_basic"+the_saved_frame+".png");
    the_saved_frame++;
    if (the_saved_frame % 5 == 0){
      println("video: " + video_num + ", frame: " + the_saved_frame);
    }
  }else if(the_saved_frame >= 900 && video_num < 12){
    the_saved_frame = 0;
    video_num++;
  }
}
