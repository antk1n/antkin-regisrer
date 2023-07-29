import React, {Component} from 'react';
import {Otsing} from './Otsing'
import {Collapsable} from './Collapsable'
import {Navigate} from 'react-router-dom';

export class Edit extends Component{
    
    constructor(props){
        super(props);
        this.state={Mylist:{}, //otsingu list
        formValues: [], // uued asutajad { isikutyyp:"", nimi: "", perenimi : "", kood: "", osauhinguOsa: "" }
        formValues2: [], //asutajad mis juba olemas { isikutyyp:"", nimi: "", perenimi : "", kood: "", osauhinguOsa: "" }
        popupMSG: "", //popup tekst
        popupState: "popup-diabled", //popup style
        redirectID: "" //isiku id, õnnestumisel leht viib tagasi Osaühingu andmete vaatele.
        };
        this.refreshList = this.refreshList.bind(this);
        this.MyhandleSubmit = this.MyhandleSubmit.bind(this);
        this.hidepopup = this.hidepopup.bind(this);
    }

    //sadame vormi
    sendForm(x){
      const requestOptions = {
        method: 'PUT',
        body: JSON.stringify(x)
      };
      fetch(process.env.REACT_APP_API +'/edit', requestOptions)
      .then(response => response.json())
      .then(data=>{
        // kontrollime, kas tagastatud error voi onnestunud msg koos id,ga
        const myArray = data.split("//");
        if (myArray[0] === "Updated Successfully"){
          this.setState({
            popupMSG: myArray[0],
            redirectID: myArray[1]
        });
        }else{
          this.setState({popupState: "popup-active-error",popupMSG:data});
        }
      }); 
    }

    // uued asutajad, muutmisel uuendame andmed 
    MyhandleChange(i, e) {
        let formValues = this.state.formValues;
        formValues[i][e.target.name] = e.target.value;
        this.setState({ formValues });
      }

      // registreeritud asutajad, muutmisel uuendame andmed 
      MyhandleChange2(i, e) {
        let formValues2 = this.state.formValues2;
        formValues2[i][e.target.name] = e.target.value;
        this.setState({ formValues2 });
      }

      //lisame veel väljad asutajate vormi
      addFormFields() {
        this.setState(({
            formValues: [...this.state.formValues, {isikutyyp:"", nimi: "", perenimi : "", kood: "", osauhinguOsa: ""}]
          }))
      }
     
      //eemaldame valjadasutajate vormist
      removeFormFields(i) {
        let formValues = this.state.formValues;
        formValues.splice(i, 1);
        this.setState({ formValues });
      }

    //kusime vajalikud andmed, lisame asutajate andmed listi
    refreshList(){
        const id = window.location.href.split("/").pop();
        let copy=[];
        fetch(process.env.REACT_APP_API +'/isik/' + id)
        .then(response => response.json())
        .then(data=>{
            this.setState({Mylist:data});
            for(let asutaja in data.asutajad){
                copy = [...copy, {isikutyyp: data.asutajad[asutaja]['isikutyyp'], nimi: data.asutajad[asutaja]['nimi'], perenimi : data.asutajad[asutaja]['perenimi'], kood: data.asutajad[asutaja]['kood'], osauhinguOsa: data.asutajad[asutaja]['osauhinguOsa']}]
                //alert(JSON.stringify(data.asutajad[asutaja]))
            }
            this.setState(({
                formValues2: [...this.state.formValues2, ...copy]
            }))
            
        });
    }

    componentDidMount(){
        this.refreshList();
    }

    //kui kasutaja vajutas 'kinnitan' nuppu, siis kontrollime ja saadame andmeid
    MyhandleSubmit(event) {
        event.preventDefault();
        let asutajadlist1 = this.state.formValues; // uued asutajad
        let asutajadlist2 = this.state.formValues2; // asutajad mis juba registreeritud
        
        const x = {
          "nimi": document.getElementById("i_nimi").value,
          "registrikood": document.getElementById("i_kood").value,
          "Asutamiskuupäev": document.getElementById("i_Asutamiskuupäev").value,
          "Kogukapital": document.getElementById("i_Kogukapital").value,
          "asutajad": this.state.formValues2,
          "uued_asutajad": this.state.formValues
        }
        //alert(JSON.stringify(x))
        //valideerimisreeglid
        var validation = this.validate(x, asutajadlist1, asutajadlist2);
        if(validation === "true"){
          //saadame
          this.sendForm(x);
        }else{
          //kuvame errori
          this.setState({
            popupMSG: validation,
            popupState: "popup-active-error"
          });
        }
      }
      
      //kontrollime sisestatud andmed
      validate(x, asutajadlist, asutajadlist2){
        var osanikutekapital = 0;
        
        if(x.Kogukapital < 2500 ){
            return "kogukapital peab olema suurem kui 2500 eur";
        }else{
            //uued asutajad
            for(var i = 0; i<asutajadlist.length;i++){
              if(asutajadlist[i].isikutyyp !== 'F' && asutajadlist[i].isikutyyp !== "J"){
                return "asutaja isikutyyp pole valitud";
              }else if(asutajadlist[i].nimi.length < 3 || asutajadlist[i].nimi.length > 100){
                return "asutaja nimi pole korrektselt taidetud, nimi peab olema 3 kuni 100 tähte või numbrit";
              }else if(asutajadlist[i].perenimi.length !== 0 && (asutajadlist[i].perenimi.length < 3 || asutajadlist[i].perenimi.length > 100)){
                return "asutaja perenimi pole korrektselt taidetud, perenimi peab olema 3 kuni 100 tähte või numbrit";
              }else if(asutajadlist[i].isikutyyp === "J" && asutajadlist[i].perenimi.length > 0){
                return "Kui isikutyyp on J, siis perenimi pole vaja taita";
              }else if(asutajadlist[i].isikutyyp === "F" && asutajadlist[i].perenimi.length === 0){
                return "Kui isikutyyp on F, siis perenimi peab olema taidetud";
              }else if(asutajadlist[i].isikutyyp === "J" && asutajadlist[i].kood.length !== 7){
                return "asutaja Registrikood pole korrektselt taidetud, Registrikood peab olema tapselt 7 numbrit";
              }else if(asutajadlist[i].isikutyyp === "F" && asutajadlist[i].kood.length !== 11){
                return "asutaja kood pole korrektselt taidetud, kood peab olema tapselt 11 numbrit";
              }else if(asutajadlist[i].osauhinguOsa < 1){
                return "asutaja osauhinguOsa peab olema vahemalt 1";
              }
              osanikutekapital = osanikutekapital + Number(asutajadlist[i].osauhinguOsa);
            }

            //juba registreeruitud asutajad
            for( i = 0; i<asutajadlist2.length;i++){
              if(asutajadlist2[i].osauhinguOsa < 1){
                return "asutaja osauhinguOsa peab olema vahemalt 1";
              }
              osanikutekapital = osanikutekapital + Number(asutajadlist2[i].osauhinguOsa);
            }

            //kapitaali kontroll
            if(osanikutekapital !== Number(x.Kogukapital)){
              return "Osanike osade suuruste summa peab olema võrdne osaühingu kogukapitali suurusega";
            }
            
            let asutajad = [...asutajadlist, ...asutajadlist2];
            let dublikaadid = [];
            var index = 0;
            //dublikaadid
            for ( i = 0; i < asutajad.length - 1; i++) {
              for (let j = i + 1; j < asutajad.length; j++) {
              if ((asutajad[i].kood === asutajad[j].kood)) {
                    dublikaadid[index] = asutajad[i];
                    index++;
                 }
              }
           }
           if(dublikaadid.length !== 0){
            return "uks inimene saab korrata ainult siis, kui duplikaat on leitud"
           }

            //kui koik on korras tagastame true
            return "true";
      }  
    }
    
    //peidame popup
      hidepopup(){
        this.setState({
          popupMSG: "",
          popupState: "popup-diabled"
        });
      }

    render(){
        const {popupState} = this.state;
        const {popupMSG} = this.state;
        const {Mylist} = this.state;
        const {redirectID} = this.state;
        return(
            <div>
              {Mylist.isosauhing === true && <div>
                {/* Kui osauhingu andmed on edukalt salvestatud, tagastab backend salvestatud osauhingu id ning edasi lehekulg viib osauhingu andmete vaatele */}
                {popupMSG === "Updated Successfully" && <Navigate to={"/info/" + redirectID} replace={true}/>}

                {/* popup ja selle msg kuvamine */}
                <div className={popupState}>
                  <label>{popupMSG}</label>
                  <button className="popup-closebtn" onClick={this.hidepopup}>X</button>
                </div>

                <h1 className='text-centered'>Edit Page</h1>
                <form  onSubmit={this.handleSubmit}>
                  <div className="container-centered">
                    <label>osauhingu nimi</label>
                    <input type="text" id="i_nimi" required={true} value={Mylist.nimi} disabled={true}/><br/>
                    <label>osauhingu registrikood</label>
                    <input type="number" id="i_kood" required={true} value={Mylist.kood} disabled={true}/><br/>
                    <label>osauhingu Asutamiskuupäev</label>
                    <input type="date" id="i_Asutamiskuupäev" required={true} value={Mylist.asutamiseKP} disabled={true}/><br/>
                    <label>Kogukapitali suurus eurodes</label>
                    <input type="number" id="i_Kogukapital" required={true} defaultValue={Mylist.kogukapital}/><br/>
                  </div>
                  
                  {/* otsing */}
                  <Collapsable className="container-centered" label="Ava otsing">
                    <Otsing text='Siis saab kontrollida mis andmed baasis olemas.'/>
                  </Collapsable>

                  {/* asutaja andmed */}
                  <div className="container-centered">
                  <h1 className='text-centered'>registreeritud asutajad</h1>
                    {this.state.formValues2.map((element, index) => (
                        <div key={index}>
                            <label>Isikutyyp</label>
                            <select name="isikutyyp" value={element.isikutyyp || ""} onChange={e => this.MyhandleChange2(index, e)} disabled={true}>
                              <optgroup>
                              <option value="" hidden disabled>Vali</option>
                              <option value="F">Fyysiline</option>
                              <option value="J">Juriidiline</option>
                              </optgroup>
                            </select>
                            <label>Nimi</label>
                            <input type="text" name="nimi" value={element.nimi || ""} onChange={e => this.MyhandleChange2(index, e)} required={true} disabled={true}/>
                            <label>Perenimi</label>
                            <input type="text" name="perenimi" value={element.perenimi || ""} onChange={e => this.MyhandleChange2(index, e)} disabled={true}/>
                            <label>Kood</label>
                            <input type="number" name="kood" value={element.kood || ""} onChange={e => this.MyhandleChange2(index, e)} required={true} disabled={true}/>
                            <label>osauhinguOsa</label>
                            <input type="number" name="osauhinguOsa" value={element.osauhinguOsa || ""} onChange={e => this.MyhandleChange2(index, e)} required={true} />                            
                        </div>
                    ))}
                    <h1 className='text-centered'>lisa veel asutajad</h1>

                    {/* uue asutajate andmed */}
                    {this.state.formValues.map((element, index) => (
                        <div key={index}>
                            <label>Isikutyyp</label>
                            <select name="isikutyyp" value={element.isikutyyp || ""} onChange={e => this.MyhandleChange(index, e)}>
                              <optgroup>
                              <option value="" hidden disabled>Vali</option>
                              <option value="F">Fyysiline</option>
                              <option value="J">Juriidiline</option>
                              </optgroup>
                            </select>
                            <label>Nimi</label>
                            <input type="text" name="nimi" value={element.nimi || ""} onChange={e => this.MyhandleChange(index, e)} required={true} minLength={3} maxLength={100}/>
                            <label>Perenimi</label>
                            <input type="text" name="perenimi" value={element.perenimi || ""} onChange={e => this.MyhandleChange(index, e)} minLength={3} maxLength={100}/>
                            <label>Kood</label>
                            <input type="number" name="kood" value={element.kood || ""} onChange={e => this.MyhandleChange(index, e)} required={true} minLength={7} maxLength={11}/>
                            <label>osauhinguOsa</label>
                            <input type="number" name="osauhinguOsa" value={element.osauhinguOsa || ""} onChange={e => this.MyhandleChange(index, e)} required={true}/>
                            <button type="button"  className="button remove" onClick={() => this.removeFormFields(index)}>Remove</button>
                        </div>
                    ))}
                    <div className="button-section">
                        <button className="button add" type="button" onClick={() => this.addFormFields()}>Lisa asutaja</button><br/><br/>
                        <label>Kinnitan, et minuga sisestatud andmed on õiged</label><br/>
                        <button className="button submit" onClick={this.MyhandleSubmit} type="submit">Kinnitan</button>
                    </div>
                  </div>
                </form>    
              </div>}           
            </div>
        )
    }
}