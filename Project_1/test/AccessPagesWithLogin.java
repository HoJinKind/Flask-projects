package Project;


import static org.junit.Assert.assertEquals;

import java.util.concurrent.TimeUnit;


import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

public class AccessPagesWithLogin {
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
			
			java.util.List<WebElement> links = driver.findElements(By.tagName("a"));
			System.out.println(links.size());
					
			// print all the links
			for (int i = 0; i < links.size(); i=i+1) {
				System.out.println(i + " " + links.get(i).getText());
				System.out.println(i + " " + links.get(i).getAttribute("href"));
			}
			
			
			// click all links in a web page
			for(int i = 0; i < links.size(); i++)
			{
				System.out.println("*** Navigating to" + " " + links.get(i).getAttribute("href"));
				if (links.get(i).getAttribute("href") == null)
					continue;
				boolean staleElementLoaded = true;
				while(staleElementLoaded) {
					try {
						driver.navigate().to(links.get(i).getAttribute("href"));
						Thread.sleep(3000);
						driver.navigate().back();
						links = driver.findElements(By.tagName("a"));
						System.out.println("*** Navigated to" + " " + links.get(i).getAttribute("href"));
						staleElementLoaded = false;
					} catch (StaleElementReferenceException e) {
						staleElementLoaded = true;
					}
				}
			}	
	  }
}

