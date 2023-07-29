/* Otsing element - otsib isiku andmeid
*
* importimiseks - import {Otsing} from './Otsing'
*
* Renderis
* <Otsing text='tekst'/>
* voi
* <Otsing />
* 
* props, mida kasutab text
* 
*/
import React, {Component} from 'react';
import './styles/main.css'

export class Otsing extends Component{
    constructor(props){
        super(props);
        this.state={Mylist:[]}
        this.refreshList = this.refreshList.bind(this);
    }

    //kusime vajalikud andmed, lisame asutajate andmed listi
    refreshList(event){
        event.preventDefault();
        const otsing = document.getElementById("otsing").value;
        const otsing_checked = document.getElementById("otsing_checked").checked;
        fetch(process.env.REACT_APP_API + '/otsing/?otsing='+otsing+'&otsing_checked='+ otsing_checked, {method: "GET"})
        .then(response => response.json())
        .then(data=>{
            this.setState({Mylist:data});
        });
    }
    render(){
        const {Mylist} = this.state;
        return(
            <div>
                {this.props.text && <label>{this.props.text}</label>}
                {/* searchbox */}
                <div className="container-centered-gray-border">
                    <h2 className='text-centered'>Otsing </h2>
                    Otsin osauhingu
                    <input type="checkbox" id ="otsing_checked"/> <br/>
                    (osauhing - true, osanik - false) <br/>
                    <input type="text" id ="otsing"/>
                    <button id ="search_btn" onClick={this.refreshList} type='button'>Otsi</button>
                </div>

                {/* kuvame andmed tabelis */}
                <div>
                    <table className='table'>
                        {Object.keys(Mylist).length !== 0 && <thead>
                            <th>Id</th>
                            <th>nimi</th>
                            <th>kood</th>
                            <th>Lisainfo</th>
                        </thead>}
                        
                        {Mylist.map(lis=>
                            <tr key={lis.id}>
                            <td>{lis.id}</td>
                            <td>{lis.nimi} {lis.perenimi}</td>
                            <td>{lis.kood}</td>
                            <td><a href={"info/" + lis.id} >Lisainfo</a></td>
                            </tr> 
                        )}
                    </table>
                </div>
            </div>
        );
    }
}