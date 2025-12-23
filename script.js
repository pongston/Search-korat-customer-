function load() {
    fetch("/data")
    .then(r=>r.json())
    .then(d=>{
        tb.innerHTML=""
        d.forEach(i=>{
            tb.innerHTML+=`
            <tr>
            <td>${i.customer}</td>
            <td>${i.site}</td>
            <td>${i.agency}</td>
            <td onclick="del(${i.id})">ลบ</td>
            </tr>`
        })
    })
}
load()

function add(){
    fetch("/add",{
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            customer:customer.value,
            site:site.value,
            agency:agency.value
        })
    }).then(load)
}

function del(id){
    fetch("/delete/"+id,{method:"DELETE"}).then(load)
}