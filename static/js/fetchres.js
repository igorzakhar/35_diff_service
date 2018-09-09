let legendHTML = `
      <div class="my-legend">
        <div class="legend-title pb-1">Legend:</div>
        <div class="legend-scale">
        <ul class="legend-labels">
          <li><span class="add"></span>Added</li>
          <li><span class="delete"></span>Deleted</li>
          <li><span class="move"></span>Moved</li>
          <li><span class="change"></span>Changed</li>
        </ul>
        </div>
      </div>
`;

function escapeHtml (string) {
  let entityMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
    '`': '&#x60;',
    '=': '&#x3D;'
  };

  return String(string).replace(/[&<>"'`=\/]/g, function (s) {
    return entityMap[s];
  });
}

let compareButton = document.getElementById("compare-button");

compareButton.addEventListener("click", function () {
  let original = escapeHtml(document.getElementById("textarea1").value);
  let changed = escapeHtml(document.getElementById("textarea2").value);

  let resultDiff = document.getElementById("diff-result") 
  
  fetch('/api/v1/htmldiff', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text1: original, 
      text2: changed,
    })
  }).then(function(response) {  

    response.json().then(function(data) {  
      resultDiff.innerHTML = "<label>Result:</label>" + data.result + legendHTML
    }).catch(function(error) {
      resultDiff.innerHTML = "<label>ERROR:</label>" + response.statusText
    });
  });

});
