var penzilla = {};
penzilla.words = {};

penzilla.words.Dictionary = function (input_id, output_id) {
    var self = this;
    self.input_id = input_id;
    self.output_id = output_id;
};

penzilla.words.Dictionary.prototype.getScrabbleWords = function () {
    var self = this;
    var input = document.getElementById(self.input_id);
    var letters = input.value;
    var resultTable = document.getElementById(self.output_id);

    var onSuccess = function(data) {
        console.log("got data");
        var resultBody = document.createElement("tbody");
        for (var e in data) {
            console.log("word: " + String(data[e][0]) + " "
                        + String(data[e][1]));
            var tr = document.createElement("tr");
            var wordTd = document.createElement("td");
            var pointsTd = document.createElement("td");
            wordTd.innerHTML = data[e][1];
            pointsTd.innerHTML = data[e][0];
            tr.appendChild(wordTd);
            tr.appendChild(pointsTd);
            resultBody.appendChild(tr);
        };
        resultTable.appendChild(resultBody);
        // remove old results
        resultTable.removeChild(resultTable.tBodies[0]);

        document.getElementById("results").style.display = "table";
    };

    console.log("letters:" + letters);
    $.getJSON("/dictionary.json?", {"letters":letters}, onSuccess);
};

penzilla.words.getScrabbleWords = function (event) {
    penzilla.dictionary.getScrabbleWords();
};