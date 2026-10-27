/* Type mode for Header -> text (docs/method/sequence-v2.md §7).
   Type the first letter of each word; the word appears when the letter is right.
   Two wrong letters on one word reveal it in red and count it as missed.
   At the end the card suggests a button; you still tap it yourself. */
(function () {
  var boxes = document.querySelectorAll('.tm-box');
  Array.prototype.forEach.call(boxes, function (box) {
    if (box.getAttribute('data-ready')) return;
    box.setAttribute('data-ready', '1');
    var input = box.querySelector('.tm-in');
    var text = box.querySelector('.tm-text');
    var score = box.querySelector('.tm-score');
    var words = Array.prototype.slice.call(box.querySelectorAll('.tw'));
    var i = 0, wrong = 0, wrongHere = 0, missed = 0, hinted = false;

    function mark() {
      words.forEach(function (w) { w.classList.remove('next'); });
      if (i < words.length) words[i].classList.add('next');
    }
    function suggestion() {
      if (hinted || missed >= 2) return 'Again';
      if (missed === 0 && wrong <= 1) return 'Good';
      return 'Hard';
    }
    function report(done) {
      var parts = [i + ' of ' + words.length + ' words', wrong + ' wrong letter' + (wrong === 1 ? '' : 's'),
                   missed + ' missed'];
      if (hinted) parts.push('hint used');
      score.textContent = parts.join(' · ') + (done || hinted ? ' → press ' + suggestion() : '');
    }
    function advance(cls) {
      words[i].classList.add(cls);
      i += 1; wrongHere = 0;
      mark(); report(i >= words.length);
    }
    function key(ch) {
      if (i >= words.length || !/[a-z0-9]/i.test(ch)) return;
      if (ch.toLowerCase() === words[i].getAttribute('data-k')) { advance('ok'); return; }
      wrong += 1; wrongHere += 1;
      text.classList.remove('wrong'); void text.offsetWidth; text.classList.add('wrong');
      if (wrongHere >= 2) { missed += 1; advance('miss'); } else { report(false); }
    }
    function start() {
      box.classList.add('tm-on');
      mark(); report(false);
      input.focus();
    }

    box.querySelector('.tm-go').addEventListener('click', start);
    box.querySelector('.tm-hint').addEventListener('click', function () {
      hinted = true;
      text.classList.add('hint');
      start();
    });
    text.addEventListener('click', function () { input.focus(); });
    // Read what was typed and clear the box, so phone keyboards can't autocorrect it.
    input.addEventListener('input', function () {
      var v = input.value; input.value = '';
      for (var k = 0; k < v.length; k++) key(v.charAt(k));
    });
  });
})();
