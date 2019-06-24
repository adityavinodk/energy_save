import React, { Component } from 'react'

class Response extends Component {
  componentDidMount () {
    if (this.props.response.category === 0) {
      document.getElementById('inference').classList.add('text-danger')
    }
    if (this.props.response.category === 1) {
      document.getElementById('inference').classList.add('text-info')
    }
    if (this.props.response.category === 2) {
      document.getElementById('inference').classList.add('text-success')
    }
  }

  render () {
    return (
      <div className='jumbotron row'>
        <div className='col-4' />
        <div className='col-4'>
          <div id='category' className='h4'>
            Category {this.props.response.category}
          </div>
          <div id='info' className='lead mb-3'>
            {this.props.response.info}
          </div>
          <div id='inference' className='font-italic mb-4'>
            {this.props.response.inference}
          </div>
          <button
            className='btn btn-success'
            onClick={() => {
              window.location.href = this.props.appliance
            }}
          >
            Fill Details Again
          </button>
        </div>
      </div>
    )
  }
}

export default Response
