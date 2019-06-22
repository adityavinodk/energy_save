import React, { Component } from 'react';

class Response extends Component {
    render() {
    return <div className="jumbotron">
      <div className="h4">Category {this.props.response.category}</div>
      <div className="lead mb-3">{this.props.response.info}</div>
      <div className="lead mb-4">{this.props.response.inference}</div>
      <button className="btn btn-success" onClick={()=>{window.location.href= this.props.appliance}}>Fill Details Again</button>
    </div>
    }
}

export default Response;