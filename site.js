
function showData(){
  fetch("files/logs/log_2024-11-08.txt")
    .then((res) => res.text())
    .then((text) => {
      console.log(text)
    })
}

async function readFile() {
  const response = await fetch("files/2dekmrledn.txt");
  const text = await response.text();
  const lines = text.split('\n');
  const namedText = lines.map(element => ({
    naam: element,
    aanwezig: 0,
    afwezig: 0
  }));
  return namedText;
}

async function makeTable(date){
  let mem = await readFile();
  
  let afwIndex = 0;
  let row = [];
  const Columns = [
    {field: 'name'},
    {field: 'aanwezig aantal'},
    {field: 'afwezig aantal'}
  ];

  date.forEach(element => {
    let aanw = 1;
    let afw  = 0;
    fetch(`files/logs/log_${date}.txt`)
    .then((res) => res.text())
    .then((text) => {
      naam = text.split('\n')
      for (let index = naam.length - 1; index > 0; index--){
        if(naam[index] == "Afwezig:"){
          afwIndex = index;
          break;
        }
      }
      for (let index = 1; index < naam.length; index++) {
        if(naam[index] == "")
          continue;
        if (index == afwIndex){
          aanw = 0;
          afw = 1;
          continue;
        }

        row.push({'name': naam[index], 'aanw': aanw, 'afw': afw});

      }
    })
  });
  console.log(row);
}

