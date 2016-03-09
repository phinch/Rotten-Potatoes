package dbloader;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class Loader {
	private Connection conn;
	
	public Loader(String dbpath) throws ClassNotFoundException, SQLException {
		Class.forName("org.sqlite.JDBC");
	    String urlToDB = "jdbc:sqlite:" + dbpath;
	    conn = DriverManager.getConnection(urlToDB);
	    Statement cstat = conn.createStatement();
	    cstat.executeUpdate("PRAGMA foreign_keys = ON;");
	}
}
