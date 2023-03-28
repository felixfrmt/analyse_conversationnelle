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
    })
    .catch(console.error);
}

function fill_stats(){
  document.getElementById("stats").innerHTML = ""

  fetch('http://127.0.0.1:8000/all_stats/')
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("stats").innerHTML += data
      
    })
    .catch(console.error);
}


async function upload_directory(){
  const files = document.getElementById("files").files;
  const formData = new FormData();

  document.getElementById("good").innerHTML = "";

  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i]);
  }

  fetch('http://127.0.0.1:8000/uploadfiles/', {
    method: 'POST',
    body: formData})
  .then((response) => response.text())
  .then((data) => {
    document.getElementById("good").innerHTML += data;
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
        console.log(right_participant)
        for (const message of data.conversation.messages) {
          console.log(message.content);
          
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
            card.setAttribute("class", "card text-bg-primary mb-3 width-75");
          }
          else {
            card.setAttribute("class", "card text-bg-secondary mb-3 width-75");
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
          console.log(div_messages.children[i])
          const div = document.createElement("div");
          // div.setAttribute("class", "w-100");
          
          const card = document.createElement("div");
          if(data.messages[i].sender == right_participant){
            div_messages.children[i].children[2].setAttribute("class", "col-5 right");  
            card.setAttribute("class", "card text-bg-primary mb-3 width-75");
          }
          else {
            div_messages.children[i].children[2].setAttribute("class", "col-5");  
            card.setAttribute("class", "card text-bg-secondary mb-3 width-75");
          };
        
          const card_body = document.createElement("div");
          card_body.setAttribute("class", "card-body");
          if (data.messages[i].sentiment_1 == ""){
            card_body.textContent += ""   
          }
          else {
            card_body.textContent += "---Sentiments--- ".concat(data.messages[i].sentiment_1, " / ", data.messages[i].sentiment_2, " ---", data.messages[i].hos, "---")
          }

          card.appendChild(card_body);
          // div.appendChild(card);
          div_messages.children[i].children[2].appendChild(card);
      }
    }
  })
  .catch(console.error);
}


