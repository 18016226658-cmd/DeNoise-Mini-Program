/*
WordCloud.js
Copyright (C) 2015  Lorenzo Cioni

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Stopwords : https://code.google.com/p/stop-words/
*/

(function() {
  //Define WordCloud constructor
  this.WordCloud = function() {
    
	// Define option defaults
    var defaults = {	 
      text: '',
      canvas : 'canvas',
      dpi: 300,
      language: 'en',
      lowerCase: false,	  
      removeDigits: true,
	  backgroundColor: '#FFF'
    }

    // Create options by extending defaults with the passed in arugments
    if (arguments[0] && typeof arguments[0] === "object") {
      this.options = extendDefaults(defaults, arguments[0]);
    }
	
	//Initialize canvas
	this.canvas = document.getElementById(this.options.canvas);
	this.context = canvas.getContext('2d');
	setCanvasDPI(this.canvas, this.options.dpi);
	this.context.rect(0, 0, this.canvas.width, this.canvas.height);
	this.context.fillStyle = this.options.backgroundColor;
	this.context.fill();
	//Array of occupied pixels
    var canvasWidth = this.canvas.width/(this.options.dpi/96);	
    var canvasHeight = this.canvas.height/(this.options.dpi/96);
    this.occupied = createMatrix(canvasWidth, canvasHeight);
  }
  
  //Define word constructor
  this.Word = function(word, color, rate, x, y){
	  //Set attributes
  	  this.text = word;
	  this.color = color;
	  this.rate = rate;
	  this.x = x;
	  this.y = y;
	  this.size = 200 * rate;
	  this.font = 'Arial';
  }
  
  /** -End constructor -- **/
  /*** Public methods ***/
  
  //Returns the keyword list from text excluding stopwords and special characters
  WordCloud.prototype.getKeywords = function(){
    var words = this.options.text.split(/\s/);
    var unchangedWords = [];
    var lowWords = [];
	  
    for(var x = 0; x < words.length; x++){
	  //Remove punctuation
      var w = words[x].match(/https?:\/\/.*[\r\n]*/g) ? 
	     words[x] : words[x].replace(/\.|,|;|!|\?|\(|\)|:|"|^'|.'|$/g,'');    
      // Remove single characters
      if(w.length === 1){
        w = w.replace(/-|_|@|&|#/g,'');
      }
      //Remove digits (if specified)
      var digitsMatch = w.match(/\d/g);
      if(this.options.removeDigits && digitsMatch && digitsMatch.length === w.length){
        w = "";
      }
      if(w.length > 0){
        lowWords.push(w.toLowerCase());
        unchangedWords.push(w);
      }
    }
    
	var keywords = [];
	this.maxFrequency = 0;
    var stopwords = getStopwords.call(this);
    for(var y = 0; y < lowWords.length; y++){
      if(stopwords.indexOf(lowWords[y]) < 0){
        var resultWord = this.options.lowerCase && !unchangedWords[y].match(/https?:\/\/.*[\r\n]*/g) ? lowWords[y] : unchangedWords[y];
		 // Build word occurrences
        if(!keywords.hasOwnProperty(resultWord)){
			keywords[resultWord] = 1;
		 } else {
			keywords[resultWord] = keywords[resultWord] + 1;
		 }
		 if(keywords[resultWord] > this.maxFrequency){
			this.maxFrequency = keywords[resultWord]; 
		 }
      }
    }
		
    return keywords;
  }
  
  //Function for drawing word on canvas
  CanvasRenderingContext2D.prototype.drawWord = function (w) {
    this.textBaseline = 'middle';
    this.font = w.size + 'px ' + w.font;
    this.fillStyle = w.color;
    this.fillText(w.text, w.x + w.size * 0.5, w.y);
    return true;
  }
    
  CanvasRenderingContext2D.prototype.getNewPosition = function(w, offsetX, offsetY){
    this.font = w.size + 'px ' + w.font;
    var width = this.measureText(w.text).width;
    var textDim = {
      width: width,
      height: w.size		
    };
	
	
	
	
	
    return textDim;
  }
  
  //Build the visual words cloud
  WordCloud.prototype.build = function(){
    var keywords = this.getKeywords();	
	var canvasWidth = this.canvas.width/(this.options.dpi/96);
	var canvasHeight = this.canvas.height/(this.options.dpi/96);
	var offsetX = canvasWidth/2;
	var offsetY = canvasHeight/2;

	for(word in keywords){
		var rate = keywords[word] / this.maxFrequency;
		rate = +(Math.round(rate + "e+" + 2)  + "e-" + 2);
		var w = new Word(word, getWordColor.call(this), rate, offsetX, offsetY)
		var previousWidth = this.context.drawWord(w);
		//offsetX += previousWidth;
	}
  }
  	

  /*** Private methods ***/
  
  function setCanvasDPI(canvas, dpi) {
    if (!canvas.style.width)
        canvas.style.width = canvas.width + 'px';
    if (!canvas.style.height)
        canvas.style.height = canvas.height + 'px';

    var scaleFactor = dpi / 96;
    canvas.width = Math.ceil(canvas.width * scaleFactor);
    canvas.height = Math.ceil(canvas.height * scaleFactor);
    var ctx = canvas.getContext('2d');
    ctx.scale(scaleFactor, scaleFactor);
	console.log('Setting canvas DPI to ' + dpi);
  }

  // Overrides default options
  function extendDefaults(source, properties) {
    var property;
    for (property in properties) {
      if (properties.hasOwnProperty(property)) {
        source[property] = properties[property];
      }
    }
    return source;
  }
  
  function createMatrix(length) {
    var arr = new Array(length || 0),
        i = length;
    if (arguments.length > 1) {
      var args = Array.prototype.slice.call(arguments, 1);
      while(i--) arr[length-1 - i] = createMatrix.apply(this, args);
    }
     return arr;
   }
  
  //Returning random color
  function getWordColor(){
	  var colors = ['#33cc33', '#000', '#0033cc', '#cc0000', '#cc00ff', '#ffff00', '#33cccc', '#660033', '#003300', '#663300'];
	  return colors[Math.floor(Math.random()*colors.length)];
  }
	
  /*** Stopwords ***/
  function getStopwords(){
    if(this.language == 'en'){
      return ["a","a's","able","about","above","after","again","against","ain't","all","allow","allows","almost","along","already","also","although","am","among","amongst","an","and","another","any","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","knows","known","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"];
     } else if(this.options.language == 'it'){
	    return ["a","ai","al","alla","allo","allora","altre","altri","altro","anche","ancora","avere","aveva","avevano","ben","buono","che","chi","cinque","comprare","con","cosa","cui","da", "dà", "del","della","dello","dentro","deve","devo","di","doppio","due","e","ecco","fare","fine","fino","fra","gente","giu","ha","hai","hanno","ho","il","indietro","invece","io","la","lavoro","le","lei","lo","loro","lui","lungo","ma","me","meglio","molta","molti","molto","nei","nella","no","noi","nome","nostro","nove","nuovi","nuovo","o","oltre","ora","otto","peggio","pero","persone","piu","poco","primo","promesso","qua","quarto","quasi","quattro","quello","questo","qui","quindi","quinto","rispetto","sara","secondo","sei","sembra","sembrava","senza","sette","sia","siamo","siete","solo","sono","sopra","soprattutto","sotto","stati","stato","stesso","su","subito","sul","sulla","tanto","te","tempo","terzo","tra","tre","triplo","ultimo","un","una","uno","va","vai","voi","volte","vostro","a","abbastanza","accidenti","ad","affinche","agli","ahime","ahimÃ","alcuna","alcuni","alcuno","all","alle","altrimenti","altrui","anni","anno","ansa","assai","attesa","avanti","avendo","avente","aver","avete","avuta","avute","avuti","avuto","basta","bene","benissimo","berlusconi","brava","bravo","c","casa","caso","cento","certa","certe","certi","certo","chicchessia","chiunque","ci","ciascuna","ciascuno","cima","cio","ciò","cioe","cioè","circa","codesta","codesti","codesto","cogli","coi","col","colei","coll","coloro","colui","come","concernente","consiglio","contro","cortesia","cos","cosi","cosÃ","d","dagli","dai","dal","dall","dalla","dalle","dallo","davanti","degli","dei","dell","delle","detto","dice","dietro","dire","dirimpetto","dopo","dove","dovra","dovrà","dunque","durante","è","ed","egli","ella","eppure","era","erano","esse","essendo","esser","essere","essi","ex","fa","fatto","favore","fin","finalmente","finche","forse","fuori","gia","già","giacche","giorni","giorno","gli","gliela","gliele","glieli","glielo","gliene","governo","grande","grazie","gruppo","i","ieri","improvviso","in","infatti","insieme","intanto","intorno","l","là","li","lontano","macche","magari","mai","male","malgrado","malissimo","medesimo","mediante","meno","mentre","mesi","mezzo","mi","mia","mie","miei","mila","miliardi","milioni","mio","moltissimo","ne","negli","nel","nell","nelle","nello","nemmeno","neppure","nessuna","nessuno","niente","non","nondimeno","nostra","nostre","nostri","nulla","od","oggi","ogni","ognuna","ognuno","oppure","ore","osi","ossia","paese","parecchi","parecchie","parecchio","parte","partendo","peccato","per","perche","perché","percio","perciò","perfino","però","piedi","pieno","piglia","più","po","pochissimo","poi","poiche","press","prima","proprio","puo","può","pure","purtroppo","qualche","qualcuna","qualcuno","quale","quali","qualunque","quando","quanta","quante","quanti","quanto","quantunque","quel","quella","quelli","quest","questa","queste","questi","riecco","salvo","sarà","sarebbe","scopo","scorso","se","seguente","sempre","si","solito","sta","staranno","stata","state","sua","successivo","sue","sugli","sui","sull","sulle","sullo","suo","suoi","tale","talvolta","ti","torino","tranne","troppo","tu","tua","tue","tuo","tuoi","tutta","tuttavia","tutte","tutti","tutto","uguali","uomo","vale","varia","varie","vario","verso","vi","via","vicino","visto","vita","volta","vostra","vostre","vostri"];
    }	
  }

}());
