function fill_select(){
  const select = document.getElementById("select_conversation");
  select.innerHTML = "";
  
  fetch('http://127.0.0.1:8000/list_id_conversations/')
    .then((response) => response.json())
    .then((data) => {
      for (const conv_id of data.list_id_conversations) {
        const listOption = document.createElement("option");
        listOption.appendChild(document.createElement("strong")).textContent = conv_id;
        listOption.setAttribute("value", conv_id)
        select.appendChild(listOption);
      }
      select.children[0].setAttribute("selected", "");
      affichage_messages();
    })
    .catch(console.error);
}

function fill_stats(){
  document.getElementById("all_stats").innerHTML = ""

  fetch('http://127.0.0.1:8000/all_stats/')
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("all_stats").innerHTML += data
      
    })
    .catch(console.error);
}


async function upload_directory(){
  const files = document.getElementById("files").files;
  const formData = new FormData();

  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i]);
  }

  fetch('http://127.0.0.1:8000/uploadfiles/', {
    method: 'POST',
    body: formData})
  .then((response) => response.text())
  .then((data) => {
      fill_select();
      fill_stats();
  })
  .catch(console.error);
}




function affichage_messages(){
  const select_value = document.getElementById("select_conversation").value;
  document.getElementById("messages").innerHTML = "";


  fetch('http://127.0.0.1:8000/list_messages/'.concat(select_value))
    .then((response) => response.json())
    .then((data) => {
      if(data != null){
        right_participant = data.conversation.participants[0];
        for (const message of data.conversation.messages) {
          
          const div = document.createElement("div");
          div.setAttribute("class", "row");          

          const div_col0 = document.createElement("div");
          div_col0.setAttribute("class", "col-5");

          const div_col1 = document.createElement("div");
          div_col1.setAttribute("class", "col-2");


          const div_col2 = document.createElement("div");
          div_col2.setAttribute("class", "col-5");          

          const card = document.createElement("div");
          if(message.sender == right_participant){
            div_col0.setAttribute("class", "col-5 right");  
            card.setAttribute("class", "card color-light mb-3 width-75");
          }
          else {
            card.setAttribute("class", "card mb-3 width-75");
          };
        
          const card_body = document.createElement("div");
          card_body.setAttribute("class", "card-body"); 
          if (message.type_message != "message"){
            card_body.textContent = "<< ".concat(message.type_message).concat(" >>");
          }
          else {
            card_body.textContent = message.content;
          }

          card.appendChild(card_body);
          div_col0.appendChild(card);
          div.appendChild(div_col0);
          div.appendChild(div_col1);
          div.appendChild(div_col2);
          document.getElementById("messages").appendChild(div);
      }
    affichage_stats_conversation();
    affichage_nlp_messages();
    }
  })
  .catch(console.error);

}



function affichage_nlp_messages(){
  const select_value = document.getElementById("select_conversation").value;
  // document.getElementById("messages").innerHTML = "";
  const div_messages = document.getElementById("messages")

  try {
    div_messages.children[3].children[2].setAttribute("class", "col-5 mx-auto p-2 loader");
  } catch (error) {
    div_messages.children[0].children[2].setAttribute("class", "col-5 mx-auto p-2 loader");
  }

  fetch('http://127.0.0.1:8000/list_nlp_messages/'.concat(select_value))
    .then((response) => response.json())
    .then((data) => {
      if(data != null){
        right_participant = data.participants[0];
        
        for (let i = 0; i < data.messages.length; i++) {
          const div = document.createElement("div");
          // div.setAttribute("class", "w-100");
          
          const card = document.createElement("div");
          if(data.messages[i].sender == right_participant){
            div_messages.children[i].children[2].setAttribute("class", "col-5 right");  
            card.setAttribute("class", "card blue-light mb-3 width-75");
          }
          else {
            div_messages.children[i].children[2].setAttribute("class", "col-5");  
            card.setAttribute("class", "card mb-3 width-75");
          };
        
          const card_body = document.createElement("div");
          card_body.setAttribute("class", "card-body");
          card_body.setAttribute("style", "padding:14px");
          switch (data.messages[i].sentiment_1) {
            case "":
              card_body.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="transparent" class="bi bi-plus-circle-fill" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/></svg>'
              break;
            case "positive":
              card_body.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="green" class="bi bi-plus-circle-fill" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/></svg>'
              break;
            case "negative":
              card_body.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="red" class="bi bi-dash-circle-fill" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/></svg>'
              break;
            case "neutral":
              card_body.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="orange" class="bi bi-slash-circle" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.646-2.646a.5.5 0 0 0-.708-.708l-6 6a.5.5 0 0 0 .708.708l6-6z"/></svg>'
              break;
            }
            // card_body.textContent += "---Sentiments--- ".concat(data.messages[i].sentiment_1, " / ", data.messages[i].sentiment_2, " ---", data.messages[i].hos, "---")

            switch (data.messages[i].hos){
              case "HATE":
                card_body.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="red" class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995z"/></svg>'
                card_body.innerHTML += '<div style="color:red; vertical-align:bottom; display:inline">HATE</div>'
                break;
              case "NON_HATE":
                card_body.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="grey" class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995z"/></svg>'                
                card_body.innerHTML += '<div style="color:grey; vertical-align:bottom; display:inline">NON HATE</div>'
                break;
              case "":
                break;
            };



          card.appendChild(card_body);
          // div.appendChild(card);
          div_messages.children[i].children[2].appendChild(card);
        };
        affichage_stats_nlp_conversation();
      };
  })
  .catch(console.error);
}




function affichage_stats_conversation(){
  const select_value = document.getElementById("select_conversation").value;
  document.getElementById("stats_conversation").innerHTML = "";


  fetch('http://127.0.0.1:8000/stats_conversation/'.concat(select_value))
    .then((response) => response.text())
    .then((data) => {
      if(data != null){
        document.getElementById("stats_conversation").innerHTML += data;
      }
  })
  .catch(console.error);
}


function affichage_stats_nlp_conversation(){
  const select_value = document.getElementById("select_conversation").value;
  document.getElementById("stats_nlp_conversation").innerHTML = "";

  fetch('http://127.0.0.1:8000/stats_nlp_conversation/'.concat(select_value))
    .then((response) => response.json())
    .then((data) => {
      if(data != null){

        // Create a new canvas to receive the chart
        var canvas1 = document.createElement('canvas');
        canvas1.setAttribute("class", "canvas");

        // Attach the canvas wherever you want
        // Note: since 2.7, the canvas can be detached when creating the chart
        const chart1 = new Chart(canvas1, {type: 'pie',
                              data: {
                              labels: ['Positif', 'Neutre', 'Négatif'],
                              datasets: [{
                                label: '# of Votes',
                                data: [data.sentiments.positive, data.sentiments.neutral, data.sentiments.negative],
                                borderWidth: 1
                              }]
                            },
                            options: {
                              scales: {
                                y: {
                                  beginAtZero: true
                                }
                              }
                            }
                          });

        // Create a new canvas to receive the chart
        var canvas2 = document.createElement('canvas');
        canvas2.setAttribute("class", "canvas");

        // Attach the canvas wherever you want
        // Note: since 2.7, the canvas can be detached when creating the chart
        const chart2 = new Chart(canvas2, {type: 'pie',
                              data: {
                              labels: ['Hate', 'No Hate'],
                              datasets: [{
                                label: '# of Votes',
                                data: [data.hos.HATE, data.NON_HATE],
                                borderWidth: 1
                              }]
                            },
                            options: {
                              scales: {
                                y: {
                                  beginAtZero: true
                                }
                              }
                            }
                          });

      document.getElementById("stats_nlp_conversation").appendChild(canvas1);
      document.getElementById("stats_nlp_conversation").appendChild(canvas2);
      }
  })
  .catch(console.error);
}