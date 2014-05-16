<?php
 
/**
 *   Example for a simple cas 2.0 client
 *
 * PHP Version 5
 *
 * @file     example_simple.php
 **/

 /*@category Authentication
 @package  PhpCAS
 @author   Joachim Fritschi <jfritschi@freenet.de>
 @author   Adam Franco <afranco@middlebury.edu>
 @license  http://www.apache.org/licenses/LICENSE-2.0  Apache License 2.0
 @link     https://wiki.jasig.org/display/CASC/phpCAS */
 
// Load the settings from the central config file
require_once 'config-simple.php';
// Load the CAS lib.  Wellesley has installed it in a central PHP library
require_once 'CAS.php';

// The following loads the Pear MDB2 class and our functions
 
require_once("MDB2.php");
require_once("/home/cs304/public_html/php/MDB2-functions.php");
 
// The following defines the data source name (username, password,
// host and database).
 
require_once('neighbrd-dsn.inc');

$dbh = db_connect($neighbrd_dsn);
 
session_start();

 
// Enable debugging
phpCAS::setDebug();
 
// Initialize phpCAS
phpCAS::client(CAS_VERSION_2_0, $cas_host, $cas_port, $cas_context);
 
// For production use set the CA certificate that is the issuer of the cert
// on the CAS server and uncomment the line below
// phpCAS::setCasServerCACert($cas_server_ca_cert_path);
 
// For quick testing you can disable SSL validation of the CAS server.
// THIS SETTING IS NOT RECOMMENDED FOR PRODUCTION.
// VALIDATING THE CAS SERVER IS CRUCIAL TO THE SECURITY OF THE CAS PROTOCOL!
phpCAS::setNoCasServerValidation();
 
// force CAS authentication
phpCAS::forceAuthentication();
 
// at this step, the user has been authenticated by the CAS server
// and the user's login name can be read with phpCAS::getUser().
 
// logout if desired
if (isset($_REQUEST['logout'])) {
    phpCAS::logout();
    die();
}
$user = phpCAS::getUser();
$strUser = strval($user);
print $strUser;

$session = strval(session_id());
print $session;

$sessionsql = "select * from usersessions where username = ?";
$resultset = prepared_query($dbh, $sessionsql, array($strUser));

if ($row = $resultset -> fetchRow(MDB2_FETCHMODE_ASSOC)) {
    $sql = "update usersessions set sessionkey = ? where username = ?";
} else {
    $sql = "insert into usersessions values (?, ?)";
}

$value = array($session, $strUser);
//$strSession = string($session);
//$strSession = strval($session)

prepared_statement($dbh, $sql, $value);
setcookie('username',$session);

//$resultset = query($dbh,$sql, $value);
 //set user in session or cookie variable
header('Location: http://cs.wellesley.edu/~neighbrd/cgi-bin/neighboard/NeighBoardPosts.cgi' ) ;
//session key in table with user name, redirect and pass in session key (randomly generated)
//generate session key and insert in php, access from python to redirect, URL includes session key, no username.
// for this test, simply print that the authentication was successful


?>
