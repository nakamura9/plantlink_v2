/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {Component} from 'react';
import styles from './tree_widget.css'


const blurredStyle = {
    backgroundColor: "#eee",
    fontWeight: "600"
}

const focusedStyle = {
    backgroundColor: '#23374d',
    color: "white"
}


export default class BaseTreeSelectWidget extends Component{
    state = {
        selected: {
            label: "None",
            id: ""
        },
        rendered: []
    }
    render(){
        return(
            <div>{this.props.data.length == 0 ?
                <h4>This list has no elements.</h4>
                : <React.Fragment>
                    <ul className={styles.root}>
                        {this.props.data.map((element, i) => {
                            console.log(element)
                            if(element.hasParent){
                                return null;
                            }else if(element.nodes.length === 0){
                                return <LeafNode
                                            focused={this.state.selected.id}
                                            node={element} 
                                            key={i}
                                            onLeafClick={this.props.branchClick}
                                            />
                            }else{
                                return <BranchNode 
                                            focused={this.state.selected.id}
                                            node={element} 
                                            key={i}
                                            mapper={this.props.dataMapper}
                                            onBranchClick={this.props.branchClick}
                                            onLeafClick={this.props.branchClick}
                                        />
                            }
                        })}
                </ul>
                </React.Fragment>}
                </div>
        );
    }
}

class BranchNode extends Component{
    state ={
        showChildren: false,
        showDropdown: false,
        highlight: false
    }

    componentDidUpdate(){
        if(this.props.focused === this.props.node.id & !this.state.highlight){
            this.setState({highlight:true})
        }
        if(this.props.focused !== this.props.node.id & this.state.highlight){
            this.setState({highlight: false});
        }
    }
    clickHandler = () =>{
        console.log('click!')
        this.setState({showChildren: !this.state.showChildren});
    }

    
    render(){
        let trasformedData = this.props.node.nodes.map(this.props.mapper);
        return(
            <li 
              style={{listStyleType: "none"}} 
              className="animated-li"
              onClick={() => this.props.onBranchClick(this.props.node, this)}
            >
                <div 
                    style={this.state.highlight ? focusedStyle : blurredStyle}
                    className={styles.node}
                    onClick={this.clickHandler}
                >
                        <span style={{margin: ".5rem"}}>
                                <i className={this.state.showChildren
                                    ? "fas fa-angle-down"
                                    : "fas fa-angle-right"}></i>
                        </span>
                        {this.props.node.label}
                </div>
                <ul style={{
                    display: this.state.showChildren ? "block" : "none"
                }}>
                    {trasformedData.map((element, i) => {
                        if(element.nodes.length === 0){
                            return <LeafNode 
                                        focused={this.props.focused}
                                        node={element} 
                                        key={i}
                                        onLeafClick={this.props.onLeafClick}
                                        />
                        }else{
                            return <BranchNode 
                                        focused={this.props.focused}
                                        node={element} 
                                        key={i}
                                        mapper={this.props.mapper}
                                        onBranchClick={this.props.onBranchClick}
                                        onLeafClick={this.props.onLeafClick}
                                    />
                        }
                    })}
                </ul>
            </li>
        );
    }
}
    

class  LeafNode extends Component{
    state = {
        showDropdown: false,
        highlight: false
    }

    componentDidUpdate(){
        if(this.props.focused === this.props.node.id & !this.state.highlight){
            this.setState({highlight:true})
        }
        if(this.props.focused !== this.props.node.id & this.state.highlight){
            this.setState({highlight: false});
        }
    }
    render(){
        return(
            <li 
                style={this.state.highlight ? focusedStyle : blurredStyle}
                className={styles.leaf_node + " animated-li-leaf"}
                onClick={() => this.props.onLeafClick(this.props.node)}>
                {this.props.node.link 
                    ? this.props.node.list 
                        ? <React.Fragment> <a href={this.props.node.link}>{this.props.node.label}</a> <a href={this.props.node.list}><i className="fa fa-list-ul"></i></a></React.Fragment>
                        : <a href={this.props.node.link}>{this.props.node.label}</a>
                    : this.props.node.label}
            </li>
        );
    }
}