import React, {Component} from 'react';
import {Navigate} from 'react-router-dom';

export class Info extends Component{
    
    constructor(props){
        super(props);
        this.state={Mylist:{},
            redirectFlag: "false"
        };
        this.refreshList = this.refreshList.bind(this);
        this.redirectEdit = this.redirectEdit.bind(this);
    }

    //kusime vajalikud andmed, lisame asutajate andmed listi
    refreshList(){
        const id = window.location.href.split("/").pop();

        fetch(process.env.REACT_APP_API +'/isik/' + id)
        .then(response => response.json())
        .then(data=>{
            this.setState({Mylist:data});
        });
    }

    componentDidMount(){
        this.refreshList();
    }

    //kui kasutaja vajutab nuppu edit nuppu, siis saadame /edit lehele 
    redirectEdit(){
        this.setState({
            redirectFlag: "true"
        });
    }

    render(){
        const {Mylist} = this.state;
        const {redirectFlag} = this.state;
        return(
            <div className="container-centered">
                {redirectFlag === "true" && <Navigate to={"/edit/" + Mylist.id} replace={true}/>}
                <h1 className='text-centered'>Infoleht</h1>
                <div>
                    id - {Mylist.id}<br/>
                    isikutyyp - {Mylist.isikutyyp}<br/>
                    isosauhing - {String(Mylist.isosauhing)}<br/>
                    nimi- {Mylist.nimi} {Mylist.perenimi}<br/>
                    kood - {Mylist.kood}<br/>
                    {String(Mylist.isosauhing) === "true" && <div>
                        asutamiseKP - {Mylist.asutamiseKP}<br/>
                        kogukapital - {Mylist.kogukapital}<br/>
                    </div>}
                </div>
                    {Mylist.isosauhing && <div>
                        <h2 className='text-centered'>Osanukud</h2>
                        <table className='table'>
                            <thead>
                                <th>id</th>
                                <th>nimi</th>
                                <th>kood</th>
                                <th>osauhinguOsa</th>
                                <th>isasutaja</th>
                            </thead>
                            {Object.values(Mylist.asutajad).map(asutaja=>
                               <tr key={asutaja.id}>
                                <td>{asutaja.id}</td>
                                <td>{asutaja.nimi} {asutaja.perenimi}</td>
                                <td>{asutaja.kood}</td>
                                <td>{asutaja.osauhinguOsa}</td>
                                <td>{String(asutaja.isasutaja)}</td>
                               </tr> 
                            )}
                        </table><br/>
                        <button type='button' onClick={this.redirectEdit}>Osakapitali suurendamise vormile</button>
                    </div>}
            </div>
        )
    }
}