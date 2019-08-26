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
    const links = this.props.response.links
    const listItems = links.map(links => (
      <li className='list-group-item'>
        <a href={links}>{links}</a>
      </li>
    ))

    const tableRows = Object.keys(this.props.response.correlatedParameters).map(
      (appliance, index) => (
        <tr>
          <td>{appliance}</td>
          <td>{this.props.response.correlatedParameters[appliance][0]}-{this.props.response.correlatedParameters[appliance][1]}</td>
        </tr>
      )
    )
    return (
      <div className='row'>
        <div className='col-3' />
        <div className='card col-6 mx-0 px-0'>
          <div id='header' className='card-header h2'>
            Energy<label className='h1 text-success'>Save</label> Report
          </div>
          <div id='body' className='card-body'>
            <div id='category' className='card-title h3'>
              Category {this.props.response.category}
            </div>
            <div id='star_range' className='card-subtitle h5'>
              Range {this.props.response.starRange}
            </div>
            <div id='info' className='lead mb-3'>
              {this.props.response.info}
            </div>
            <div id='inference' className='font-italic mb-4 text-info'>
              {this.props.response.inference}
            </div>
            <hr class='my-4' />
            <table class='table'>
              <thead class='thead-dark'>
                <tr>
                  <th scope='col'>Parameter</th>
                  <th scope='col'>Range</th>
                </tr>
              </thead>
              <tbody>
                {tableRows}
              </tbody>
            </table>
            <hr class='my-4' />
            <div id='links'>
              <label className='h4'>Helpful Links</label>
              <ul className='list-group'>{listItems}</ul>
            </div>
          </div>
          <div id='footer' className='card-footer'>
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
      </div>
    )
  }
}

export default Response
