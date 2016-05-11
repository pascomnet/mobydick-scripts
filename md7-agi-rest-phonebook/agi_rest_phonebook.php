#!/usr/bin/php5 -q
<?php
require_once '/var/www/mobydickcmd/cmn/vendor/phphttpclient/httpful.phar';

$REST_API_KEY = 'your_rest_api_key';

/**
 * this AGI executs an REST request
 * @param $arg1 uri - URI, welche gerufen werden soll
 */
ob_implicit_flush( false );
set_time_limit( 10 );
error_reporting(0);
define ('__DEBUG__', true);

// create file handles if needed
if ( !defined( 'STDIN' ) )
    define( 'STDIN', fopen( 'php://stdin', 'r' ) );
if ( !defined( 'STDOUT' ) )
    define( 'STDOUT', fopen( 'php://stdout', 'w' ) );
if ( !defined( 'STDERR' ) )
    define( 'STDERR', fopen( 'php://stderr', 'w' ) );

// URI
if ( empty( $argv[ 1 ] ) ) {
    pushVariable( 'HASH(AGI_REST_PHONEBOOK,ERRNO)', 255 );
    pushVariable( 'HASH(AGI_REST_PHONEBOOK,ERRMSG)', 'no phonenumber' );
    fclose( STDIN );
    fclose( STDOUT );
    fclose( STDERR );
    exit( 1 );
}
$phonenumber = $argv[ 1 ];
$uri = "http://tel.search.ch/api/?" . http_build_query(array('was' => $phonenumber, 'key' => $REST_API_KEY));
/** @var httpful\Response $response */
$response = \Httpful\Request::get($uri)
    ->sendsAndExpects('application/atom+xml')
    ->autoParse(false)
    ->send();

if ($response->hasErrors()) {
    pushVariable( 'HASH(AGI_REST_PHONEBOOK,ERRNO)', 255 );
    pushVariable( 'HASH(AGI_REST_PHONEBOOK,ERRMSG)', 'rest error' );
    fclose( STDIN );
    fclose( STDOUT );
    fclose( STDERR );
    exit( 1 );
}
$xml = simplexml_load_string($response->body, "SimpleXMLElement", 0, "", true);
$name = $xml->entry[0]->title;
if($name) {
    pushVariable('HTTP_CALLER_ID', $name);
}
fclose( STDIN );
fclose( STDOUT );
fclose( STDERR );
exit( 0 );

/**
 * create the right output to set a channel variable
 * @param $name
 * @param $value
 */
function pushVariable( $name, $value )
{
    fwrite( STDOUT, "SET VARIABLE " . trim( $name ) . " \"" . trim( $value ) . "\" \n" );
    fflush( STDOUT );
}
