
function showData(){
  fetch("files/logs/log_2025-03-12.txt",{
    mode: 'no-cors',
  })
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


function displayTable(row) {
  const tableBody = document.getElementById("data-table").getElementsByTagName("tbody")[0];
  tableBody.innerHTML = "";
  console.log(row);
  for (let entry in row){
    const rowElement = document.createElement("tr");
    
    const naamCell = document.createElement("td");
    naamCell.textContent = row[entry].naam;
    naamCell.style.fontWeight = "bold";
    rowElement.appendChild(naamCell);
    
    const aanwCell = document.createElement("td");
    aanwCell.textContent = row[entry].aanwezig;
    rowElement.appendChild(aanwCell);
    
    const afwCell = document.createElement("td");
    afwCell.textContent = row[entry].afwezig;
    rowElement.appendChild(afwCell);
    
    tableBody.appendChild(rowElement);
  }
}

// Takes the dates given, looks up the corresponding logs and then 
// makes a table with the processed data
async function makeTable(date){
  let afwIndex = 0;
  let row = [];
  let first = true;
  // Loop through the given files
  for (const element of date){
    
    let aanw = 1;
    let afw  = 0;
    // Get the correct file
    const res = await fetch(`files/logs/log_${element}.txt`);
    const text = await res.text();
    
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
      if (index == afwIndex)
      {
        aanw = 0;
        afw = 1;
        continue;
      }
      // If this is the first logfile being parsed just push the names etc into the file
      if(first)
      {
        row.push({'naam': naam[index], 'aanwezig': aanw, 'afwezig': afw});
      }
      // If the logfile is not the first increment the existing one
      else
      {
        const entry = row.find(entry => entry.naam === naam[index]);
        if(entry)
        {
          entry.aanwezig += aanw;
          entry.afwezig += afw;
        }
      }
    }
    first = false;
    if(date[0] === date[1])
      return row;
  }
  return row;
} 
    
async function table(date){
  let row = await makeTable(date);
  displayTable(row);
}