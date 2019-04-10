package Project;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class AccessPageWithLogin {
	 private WebDriver driver;
	 
	  private StringBuffer verificationErrors = new StringBuffer();

	  @Before
	  public void setUp() throws Exception {
	    driver = new FirefoxDriver();
	    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	  }

	  
	  @Test
	  public void testAccessHomePageWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
			
		    driver.get("http://35.198.199.181:5000/home");
		    assertEquals ("home", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessRoomPageWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
			
		    driver.get("http://35.198.199.181:5000/room");
		    assertEquals ("room", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessGeneratePageWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
			
		    driver.get("http://35.198.199.181:5000/generate");
		    assertEquals ("generate", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessConstraintsPageWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
			
		    driver.get("http://35.198.199.181:5000/constraints");
		    assertEquals ("constraints", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessConstraint_ProfPageWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
	    driver.get("http://35.198.199.181:5000/constraint_Prof");
	    assertEquals ("Prof/ Weekly constraints", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessConstraint_OnePageWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
	    driver.get("http://35.198.199.181:5000/constraint_OneTime");
	    assertEquals ("Onetime constraints", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessConstraint_ViewWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
	    driver.get("http://35.198.199.181:5000/constraints_View");
	    assertEquals ("constraints_View", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessViewPageWithLogin() throws Exception {
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://35.198.199.181:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
			
		    driver.get("http://35.198.199.181:5000/view");
		    assertEquals ("view", driver.getTitle());
	  }
	  
}
	  
