var req;
function searchbook(temp){
    req=new XMLHttpRequest();
    req.onreadystatechange=output;
    req.open("GET","getbook?temp="+temp,true);
    req.send();
}

function output(){
    if(req.readyState==4 && req.status==200){
        bklist=JSON.parse(req.responseText);
        tbody=document.getElementById("tbody");
        tbody.innerText=""
        for(bk of bklist){
            tr=document.createElement("tr");

            td1=document.createElement("td")
            td1.innerText=bk.book_id
            tr.appendChild(td1)

            td2=document.createElement("td")
            td2.innerText=bk.bName
            tr.appendChild(td2)

            td3=document.createElement("td")
            td3.innerText=bk.author
            tr.appendChild(td3)

            td4=document.createElement("td")
            td4.innerText=bk.publisher
            tr.appendChild(td4)

            td5=document.createElement("td")
            td5.innerText=bk.category
            tr.appendChild(td5)

            td6=document.createElement("td")
            td6.innerText=bk.edition
            tr.appendChild(td6)

            td7=document.createElement("td")
            td7.innerText=bk.count
            tr.appendChild(td7)

            // td8=document.createElement("td")
            // a1=document.createElement("a")
            // a1.innerHTML='<i class="fa-solid fa-pen-to-square"></i>'
            // a1.setAttribute("href" ,"{% url 'editbook' id="+bk.book_id+"%}" )
            // a1.setAttribute("class" , "accept")
            // td8.appendChild(a1)
            // tr.appendChild(td8)

            // td9=document.createElement("td")
            // a2=document.createElement("a")
            // a2.innerHTML='<i class="fa-solid fa-trash"></i>'
            // a2.setAttribute("href" ,"{% url 'delbook' id=bk.book_id %}" )
            // a2.setAttribute("class" , "reject")
            // td9.appendChild(a2)
            // tr.appendChild(td9)

            tbody.appendChild(tr)
            console.log(bk.book_id)

        }
    }
}
