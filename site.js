
function showData(){
  fetch("files/logs/log_2024-11-08.txt")
    .then((res) => res.text())
    .then((text) => {
      console.log(text)
    })
}

function makeTable(link){
  fetch(link)
  .them((res) => res.text())
  .then((text) => {
  
  })
}