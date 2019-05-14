let bookstyle = {
  "n": 'novel',
  "r": "refer",
  "i": "image"
};

function entryOpen() {
  if (document.getElementById('book-type')) {
    let target = document.getElementById('book-type').value;

    for (var type in bookstyle) {
      let formSet = document.getElementsByClassName(bookstyle[type]);
      for (var i = 0, len = formSet.length; i < len; i++) {
        if (type == target) {
          formSet.item(i).style.display = "";
        } else {
          formSet.item(i).style.display = "none";
        }
      }
    }
  }
}
function swPrevBookShow(){
  let checkPrevBook = document.getElementById('prevBook');
  let listPrevBook = document.getElementById('prevRecBooks');
  let selectZone = document.getElementById("novel-genre-select");
  console.log(checkPrevBook.checked)
  if(checkPrevBook.checked == true){
    listPrevBook.style.display = "";
    selectZone.style.display = "none";
  }else{
    listPrevBook.style.display="none";
    selectZone.style.display = "";
  }
}

//Flaskからの値受け取り
let prevAns ={{ prevAns|tojson }}; // 前回の解答
console.log(prevAns); // Flask表記
let histLoad = function() {
  if (prevAns.length > 0) {
    // 値の受け取り
    let btype = prevAns['btype'];
    let chosenGenre = prevAns['genreSelect'];
    let bookLen = prevAns['storyLen'];
    let tempo = prevAns['tempo'];
    let count = prevAns['rentaCount'];
    // 受信の確認

    /*フォームの切り替え*/
    let prevForm = document.forms.anqSheet;
    prevForm.btypeSelect.btype.value = btype; //選択部分
    let formType = document.getElementsByClassName(btype)
    // ジャンル選択
    let genreChoose = formType.item(0).getElementsByName('genreSelect')
    for (var i = 0, len = genreChoose.length; i < len; i++) {
      var v = genreChoose.item(i).value;
      for (genre in chosenGenre) {
        if (v == genre) genreChoose.item(i).checked = True;
      }
    }
    //テンポ
    let bookTempo = formType.item(1).getElementsByTagName('input');
    bookTempo.value = tempo;

    //本の長さ
    let rangeForm = document.getElementsByName('range')
    rangeForm.value = bookLen;

    //貸出回数
    let countForm = document.getElementsByName('rentaCount');
    countForm.value = count;

  } else {
    console.log('No History');
  }
  let preBooksName = {{ prevBook|tojson }}; //前回の推薦データ
  if (preBooksName.length > 0) {
    let preBookShowZone = document.getElementById('prevRecView')
    var optBooks = preBookShowZone.children
    for (var i = 0; i < optBooks.length; i++){
      optBooks[i].value = preBooksName[i]
      console.log(optBooks[i].value)
    }
  } else {
    console.log('No preBooks')
  }
  let firstFlag = {{ firstFlag|tojson }}
  if (firstFlag != 0){
    console.log('FisrtRecommend');
    let preBookDiv = document.getElementsByClassName('preBook');
    for(var i=0; i<preBookDiv.length; i++){
      preBookDiv.item(i).style.display = "none";
    }
  }
  entryOpen();
  swPrevBookShow();
};
window.onload = histLoad;
