/* Collapsable element - peidab/naitab sees olev kontekst
*
* importimiseks - import {Collapsable} from './Collapsable'
*
* Renderis
* <Collapsable className="container-centered" label="Ava otsing">
*  **kontekst**
* </Collapsable>
*
* props, mida kasutab className, label, children
* 
*/

import React, {Component} from 'react';

export class Collapsable extends Component{
    constructor(props) {
        super(props);
        this.state = {
          open: false
        };
        this.toggle = this.toggle.bind(this);
    }
    
    //kuvada voi peida 
    toggle() {
        if (this.state.open === false){
            this.setState({
                open: true
            });
        }else{
            this.setState({
                open: false
            });
        }
        
      };

    render(){
        const {open} = this.state;
        return(
            <div className={this.props.className}>
                <button type='button' onClick={this.toggle}>{this.props.label}</button>
                {open && <div>{this.props.children}</div>}
            </div>
        );
    }
}

export default Collapsable;